# Distributed Color Assignment Demo

This example uses **Vagrant** + **Docker** to assign nodes
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
     - Build a Python-based client image from `./client` and start multiple client containers (`client-1`, `client-2`, etc.).  
   - Watch the logs in your terminal to see each client discover other nodes and choose `green` or `red`.
4. **Check** how containers are doing:
   - `docker ps` or `vagrant global-status`
5. **Cleanup** with `vagrant destroy -f`.

## How it Works

- Each client container runs the Python script `color-broadcast.py`.
- The script uses UDP broadcasts to discover other nodes in the network.
- All nodes wait until every node has been discovered before proceeding.
- After discovery, each node sorts the list of all IP addresses.
- Based on position in the sorted list and the COLOR_RATIO, each node determines whether it should be "green" or "red".
- By design, at most `floor(RATIO*N)` nodes end up assigned green, and the rest are red, **without** a central coordinator.

