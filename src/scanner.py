import socket
import ipaddress
import struct
import random
import re
import fcntl
from packet import Packet

class Scanner():
    def __init__(self, client_server,protocol=None, range="127.0.0.1", port=65432, interface='eth0'):
        self.range = range              # IP or CIDR IP range
        self.protocol = protocol        # TCP or UDP - most scans will be TCP 
        self.port = port                # Port or port range
        self.src_port = random.randint(40000, 55000)
        self.client_server = client_server
        self.port = self._determine_ports()
        self.range = self._determine_range()
        self.local = self._get_local_ip(interface)

    def scan(self):
        open_ports = {}
        for ip in self.range:
            for port in self.port:
                flags = Packet(self.src_port, port, src=self.local ,dst=ip).send_packet()
                if flags:
                    if ip not in open_ports.keys():
                        open_ports[ip] = []
                    open_ports[ip].append(port)
        self._format_output(open_ports)
    
    def _format_output(self, open_ports):
        for host in open_ports.keys():
            print("-" * 50)
            print("Host" + (" " * 12) + "Port" + (" " * 12) + "State")
            print("-" * 50)
            for port in open_ports[host]:
                print(host + (" " * 6) + f"{port}" + (" " * 12) + "open")
                

    def _determine_range(self):
        # Parses IP input to create a range of IP addresses in a list 
        # Currently can process cidr. Comma ranges and hyphenated ranges may only appear at the end.
        # Not sure how to provide full functionality for comma + hyphen ranges like nmap has. 
        ips = []
        single_ip = re.compile(r"\b([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\b(?!\/|\-|,[0-9]{1,3})")
        cidr_range = re.compile(r"\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}\b")
        oct_range = re.compile(r"\b(?:[0-9]{1,3}(?:-[0-9]{1,3})?\.){3}[0-9]{1,3}(?:-[0-9]{1,3})\b")
        comma_range = re.compile(r"\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(?:,[0-9]{1,3})+\b")
        cidr = re.findall(cidr_range, self.range)
        oct = re.findall(oct_range, self.range)
        comma = re.findall(comma_range, self.range)
        if oct:
            for ip in oct:
                start,end,octet = 0,0,0
                octets = ip.split('.')
                for i in range(len(octets)):
                    if '-' in octets[i]:
                        octet = i
                        start_end = octets[i].split('-')
                        start,end = int(start_end[0]), int(start_end[1])
                        end = int(start_end[1])
                for i in range(start, end + 1):
                    octets[octet] = str(i)
                    ips.append(".".join(octets)) 
        if cidr:
            for ip in cidr:
                network = ipaddress.IPv4Network(ip)
                for addr in network:
                    if addr != network.network_address and addr != network.broadcast_address:
                        ips.append(format(addr))
        if comma:
            for ip in comma:
                base_plus_hosts = ip.split(".")
                commas = []
                octet = 0
                for i in range(len(base_plus_hosts)):
                    if "," in base_plus_hosts[i]:
                        octet = i
                        commas.extend(base_plus_hosts[i].split(","))
                for i in range(len(commas)):
                    base_plus_hosts[octet] = commas[i]
                    ips.append(".".join(base_plus_hosts))
        ips.extend(re.findall(single_ip, self.range))
        print(ips)
        return ips

    def _determine_ports(self):
        # Parses port input to create a list of ports
        self.port = self.port.split(',')
        new_ports = []
        for port in self.port:
            if '-' in port:
                port = port.split('-')
                port = [num for num in range(int(port[0]), int(port[1]) + 1)]
                for i in port:
                    new_ports.append(i)
            else:
                new_ports.append(int(port))
        return new_ports

    def _get_local_ip(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        raw_bytes = fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', ifname[:15].encode())
        )[20:24]\
        
        return raw_bytes