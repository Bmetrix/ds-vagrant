#!/usr/bin/env python3
"""
color-broadcast.py

Simple approach to color assignment without ZooKeeper or a coordinator:
1) Each node broadcasts "HELLO <ip>" on UDP port 9999.
2) Each node listens for others' broadcasts until all expected nodes are discovered.
3) Sort the IP list. The first floor(k*N) => 'green', the rest => 'red'.
"""

import os
import socket
import time
import threading
from datetime import datetime

BROADCAST_PORT = 9999

def broadcast_loop(my_ip):
    """Thread that periodically broadcasts 'HELLO <my_ip>'."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Enable broadcast
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        msg = f"HELLO {my_ip}"
        # 255.255.255.255 is the limited broadcast address
        sock.sendto(msg.encode('utf-8'), ('255.255.255.255', BROADCAST_PORT))
        time.sleep(1.0)

def main():
    # Env variables:
    node_name      = os.environ.get("NODE_NAME", "client-???")
    color_ratio    = float(os.environ.get("COLOR_RATIO", "0.5"))
    discovery_time = int(os.environ.get("DISCOVERY_TIME", "5"))
    nodes_count    = int(os.environ.get("NODES_COUNT", "1"))

    # Attempt to find our own IP:
    # (In Docker, gethostname() might give container's internal hostname, which
    #  hopefully resolves to an IP on the colors-net network.)
    my_ip = socket.gethostbyname(socket.gethostname())
    print(f"[{node_name}] My IP is {my_ip}, ratio={color_ratio}, discoveryTime={discovery_time}, expectedNodes={nodes_count}")

    # 1) Start the broadcast thread
    th = threading.Thread(target=broadcast_loop, args=(my_ip,), daemon=True)
    th.start()

    # 2) Listen for incoming broadcasts on UDP port 9999
    discovered = set()
    discovered.add(my_ip)  # include ourselves
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind on all interfaces, port 9999
    # Note: Docker or some networks may require "0.0.0.0"
    sock.bind(('', BROADCAST_PORT))

    print(f"[{node_name}] Listening for UDP broadcasts on port {BROADCAST_PORT}...")
    print(f"[{node_name}] Waiting to discover all {nodes_count} nodes...")

    # Continue listening until we've discovered all expected nodes
    # or until the discovery timeout is reached
    start_time = time.time()
    while len(discovered) < nodes_count and (time.time() - start_time < discovery_time):
        sock.settimeout(1.0)  # check once per second
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode('utf-8', errors='ignore').strip()
            if msg.startswith("HELLO "):
                ip = msg.split(" ", 1)[1]
                if ip not in discovered:
                    discovered.add(ip)
                    print(f"[{node_name}] Discovered node with IP: {ip} ({len(discovered)}/{nodes_count})")
        except socket.timeout:
            pass

    if len(discovered) < nodes_count:
        print(f"[{node_name}] Warning: Discovery time elapsed, but only found {len(discovered)}/{nodes_count} nodes.")
    else:
        print(f"[{node_name}] Successfully discovered all {nodes_count} nodes.")

    # 3) Now we have a set of discovered IPs
    all_ips = sorted(discovered)

    N = len(all_ips)
    green_capacity = int(color_ratio * N)

    # 4) Our index in the sorted list => color
    my_index = all_ips.index(my_ip)
    color = "green" if my_index < green_capacity else "red"

    print(f"[{node_name}] Discovered {N} IPs -> {all_ips}")
    print(f"[{node_name}] My index={my_index}, => color={color}")

    # 5) Keep container alive so we can see logs
    print(f"[{node_name}] Done color assignment. Sleeping 300s so container won't exit.")
    time.sleep(300)

if __name__ == "__main__":
    main()
