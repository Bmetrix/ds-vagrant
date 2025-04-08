#
# Simple backend service demo
#

from time import sleep
from scapy.all import *

def main():
    while True:
        print("Hello from leader")
        packet = IP(dst="10.0.1.255")/UDP(dport=500)/"Hello from leader"
        send(packet)
        sleep(5)

main()

# potom jsme se pripojili pres 'vagrant ssh follower-1' (na follower-1) a tam sudo python3 >> from scapy.all import * >> p = sniff(count=2, filter="udp") -> pro sniffer (nebo wireshark) je nutný mít DOKCER (ALE NE DESKTOP ALE NATIVNÍ!!!) 
# POKUD NENÍ NATIVNÍ DOCKER TAK POUŽÍT: sudo tcpdump -i eth1 -X -> pak výpis:

"""

Což je výpis z hello packetu od leadera:

    12:11:34.403435 IP leader.vagrant_network_10.0.1.0/24.domain > 10.0.1.255.isakmp: 18533 updateMA [b2&3=0x6c6c] [26226a] [28448q] [28525n] [8300au] [|domain]
    0x0000:  4500 002d 0001 0000 4011 63b7 0a00 010a  E..-....@.c.....
    0x0010:  0a00 01ff 0035 01f4 0019 9085 4865 6c6c  .....5......Hell
    0x0020:  6f20 6672 6f6d 206c 6561 6465 72         o.from.leader

"""

# EOF
