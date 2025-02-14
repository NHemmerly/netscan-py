# netscan-py

## Overview

My plan for this project is to create a robust port scanning tool using Python. Taking clear inspiration from [nmap](https://nmap.org/). I chose to do this as my first personal project for my [boot.dev](https://www.boot.dev/tracks/backend) backend programming course. My goals for this project are to learn more about how packets are built and sent by applications, and to gain a little bit of insight into what is happening under the hood in tools like nmap. 

I'm deeply interested in information security, so this project felt like a logical choice.

### Building a Packet

A packet in computer networking basically refers to the *envelope* that contains information about how to get information from one computer to another as well as the actual information that a set of computers want to communicate. Packets are made up of different levels of headers, this project builds custom IP and TCP headers to send a simple TCP packet across the network. An IP header is a 20 byte long structure that contains information about the IP version, the source address, the destination address, the protocol used, along with a checksum and other information. A TCP header is a 20 to 60 byte long structure that includes source and destination ports, flags that define the type of connection they're building, as well as a checksum and other information. 

Packets are built in the Packet class in packet.py using information provided by the user on the command line. The scanner class parses information from the user and builds a list of IP addresses and ports to scan. The program iterates over every IP address and every port specified to build a SYN packet for each IP address and port, calculating IP and TCP header checksums along the way. After a packet is built, it is immediately sent over the network to its destination while the host computer waits 0.2 seconds for a response. Once the host receives a response it checks if the *SYN* and *ACK* flags were present in the response (indicating a response from the target, and likely an open port). Once a *SYN-ACK* packet is received, the host replies with a *RST* flagged packet immediately tearing down the handshake and recording an *open* response.

## Usage

`sudo python3 src/main.py -r <ip or ip-range> -p <port or port-range> -v <true or false>`

### Output
```
--------------------------------------------------
Host            Port            State
--------------------------------------------------
192.168.1.2      22             open
192.168.1.2      80             open
192.168.1.2      135            open
192.168.1.2      139            open

```

## Outcomes

I learned a lot about TCP/IP during this project so far. I used a lot of information from existing projects that build custom packets in Python (my packet class takes almost verbatim from ["Creating a SYN port scanner"](https://inc0x0.com/tcp-ip-packets-introduction/tcp-ip-packets-4-creating-a-syn-port-scanner/)). I also learned about a few helpful builtin Python modules such as *asyncio*, *socket*, *argparse*, *ipaddress*, and *struct*. 

### Improvements

- While I included some error-handling in this project, there could certainly be more. 
- Options for checking versions of applications would be very interesting to learn about and include. 
- Parsing IP addresses entered by the user could definitely be improved. 



