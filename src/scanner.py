import socket

class Scanner():
    def __init__(self, protocol, range, port=None):
        self.range = range              # IP or CIDR IP range
        self.protocol = protocol        # TCP or UDP - most scans will be TCP 
        self.port = port                # Port or port range

    def _determine_range(self):
        # Function for parsing ip range into a list of IPs to scan
        pass

    def _determine_ports(self):
        # function for parsing port input into a list of ports to scan
        pass