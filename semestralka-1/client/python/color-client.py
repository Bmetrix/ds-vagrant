#!/usr/bin/env python3
"""
color-client.py

Each node tries to assign itself 'green' or 'red' so that we end up with
floor(k*N) green and the rest red. No single coordinator is used; each node
consults ZooKeeper state, attempts ephemeral creation, and handles races.
"""

import os, socket, random
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError, NoNodeError

def main():
    # 1) Read environment variables from Docker
    ensemble     = os.environ.get("ZOO_SERVERS", "localhost:2181")
    node_name    = os.environ.get("NODE_NAME", socket.gethostname())
    total_nodes  = int(os.environ.get("TOTAL_NODES", "6"))
    color_ratio  = float(os.environ.get("COLOR_RATIO", "0.5"))

    # 2) Compute how many "green" vs "red" slots
    green_capacity = int(round(color_ratio * total_nodes))
    red_capacity   = total_nodes - green_capacity

    print(f"[{node_name}] Starting up, connecting to ZK at {ensemble}")
    zk = KazooClient(hosts=ensemble)
    zk.start()

    # 3) Ensure the base paths exist
    for path in ["/color_assignments", "/color_assignments/green", "/color_assignments/red"]:
        try:
            zk.create(path, makepath=True)
        except:
            pass  # ignore if already exists

    # Helper to count how many ephemeral children exist in a color path
    def count_color(c):
        try:
            return len(zk.get_children(f"/color_assignments/{c}"))
        except NoNodeError:
            return 0

    assigned_color = None
    while True:
        green_count = count_color("green")
        red_count   = count_color("red")

        print(f"[{node_name}] Current usage: GREEN={green_count}/{green_capacity}, RED={red_count}/{red_capacity}")

        # how many slots left
        green_slots = green_capacity - green_count
        red_slots   = red_capacity - red_count

        if green_slots <= 0 and red_slots <= 0:
            print(f"[{node_name}] Both colors are full. No assignment possible.")
            break

        # If both have room, pick randomly. If only one has room, pick that.
        possible_colors = []
        if green_slots > 0:
            possible_colors.append("green")
        if red_slots > 0:
            possible_colors.append("red")

        attempt_color = random.choice(possible_colors)
        path = f"/color_assignments/{attempt_color}/{node_name}"
        print(f"[{node_name}] Attempting color={attempt_color} at path={path}")

        try:
            # 4) Create ephemeral znode => final lock-in if it succeeds
            zk.create(path, ephemeral=True)
            print(f"[{node_name}] SUCCESS: assigned color={attempt_color}")
            assigned_color = attempt_color
            break
        except NodeExistsError:
            # If the node_name is already used, append a suffix (rare unless repeated node_name)
            print(f"[{node_name}] NodeExistsError - will retry with random suffix.")
        except Exception as e:
            # Possibly the color got filled up between checking and creation
            print(f"[{node_name}] Failed ephemeral create. Reason: {e}, retrying...")

    if assigned_color:
        print(f"[{node_name}] Assigned color={assigned_color}. Holding ephemeral node...")
        # keep the session alive so ephemeral node remains
        try:
            zk.sleep(300)  # e.g. stay active for 5 min or until container stops
        except KeyboardInterrupt:
            pass
    else:
        print(f"[{node_name}] Not assigned any color. Exiting.")

    zk.stop()

if __name__ == "__main__":
    main()
