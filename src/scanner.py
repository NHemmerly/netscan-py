import socket
import struct
import fcntl
import binascii
from packet import Packet

class Scanner():
    def __init__(self, client_server,protocol=None, range="127.0.0.1", port=65432, interface='eth0'):
        self.range = range              # IP or CIDR IP range
        self.protocol = protocol        # TCP or UDP - most scans will be TCP 
        self.port = port                # Port or port range
        self.client_server = client_server
        self.port = self._determine_ports()
        self.local = self._get_local_ip(interface)

    def _determine_range(self):
        # Function for parsing ip range into a list of IPs to scan
        pass

    def _determine_ports(self):
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

    def scan(self):
        for port in self.port:
            flags = Packet(port, src=self.local ,dst=self.range).send_packet()
            if flags == 18:
                print(f"Port {port} is open")
            #else:
                #print(f"Port {port} is closed")

    def _server(self):
        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)

    def _client(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.sendto(self.packet.packet, (self.range, 0))
        data = s.recvfrom(65535)
        s.close()
        
        return data