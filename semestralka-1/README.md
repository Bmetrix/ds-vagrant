# Distributed Color Assignment Demo

This example uses **Vagrant** + **Docker** + **ZooKeeper** to assign nodes
into two colors ("green" / "red") at a ratio `COLOR_RATIO` with **no single coordinator**.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)  
- [Vagrant](https://developer.hashicorp.com/vagrant/downloads)  
- (On Windows, you can use [WSL2](https://docs.microsoft.com/en-us/windows/wsl/))

## Usage

1. **Clone** or copy this `semestralka-1` folder.  
2. **Open a terminal** in `semestralka-1`.  
3. Run `vagrant up`.  
   - This will:
     - Pull the official `zookeeper:3.7` image and start one ZooKeeper container named `zoonode`.
     - Build a Python-based client image from `./client` and start multiple client containers (`client-1`, `client-2`, etc.).  
   - Watch the logs in your terminal to see each client attempt to choose `green` or `red`.
4. **Check** how containers are doing:
   - `docker ps` or `vagrant global-status`
5. **Cleanup** with `vagrant destroy -f`.

## How it Works

- A single ZooKeeper container listens on port 2181.  
- Each client container runs the Python script `color-client.py`.  
- The script checks how many ephemeral znodes currently exist for `green` vs. `red`, and tries to create a new ephemeral node in whichever color still has capacity.  
- By design, at most `floor(RATIO*N)` nodes end up assigned green, and the rest are red, **without** a coordinator. Race conditions are resolved by ephemeral node creation failing or succeeding atomically.

