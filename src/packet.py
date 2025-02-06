import socket
# A class to create custom packet objects depending on the type of service
# being scanned. Can create custom packets as well as parse incoming packets.

class Packet():
    def __init__(self, src="127.0.0.1", dst="127.0.0.1", port=65432):
        self.ip_header = []
        self.src = src
        self.dst = dst
        self.port = port
        # IP packet
        self.version =          b'\x4'
        self.ihl =              b'\x5'
        self.tos =              b'\x00'
        self.total_len =        b'\x00\x34'
        self.identification =   b'\x8e\x7c'
        self.flags =            b'\x4000'
        self.ttl =              b'\x40'
        self.protocol =         b'\x06'
        self.header_checksum =  b'\x00'
        
        self.build_syn()
        self._ip_header_checksum = self._get_header_checksum()

    def build_syn(self):
        self.ip_header.append(b'\x45\x00') #ip_header[0]
        self.ip_header.append(b'\x00\x34') #ip_header[1]
        self.ip_header.append(b'\x8e\x7c') #ip_header[2]
        self.ip_header.append(b'\x40\x00') #ip_header[3]
        self.ip_header.append(b'\x40\x06') #ip_header[4] <- header checksum inserted here
        self.ip_header.append(b'\xac\x1c') #ip_header[5]
        self.ip_header.append(b'\xb0\x53') #ip_header[6]
        #self.ip_header.append()                    #ip_header[4]


    #0000   00 15 5d 48 46 12 00 15 5d 88 fd 00 08 00 45 00
    #0010   00 34 8e 7c 40 00 40 06 12 c6 ac 1c b0 53 0a 03
    #0020   33 0f c1 88 00 87 d3 e0 bb 7a 52 9c 5d 83 80 10
    #0030   01 f8 ea 86 00 00 01 01 08 0a af f6 3b ef 0a 72
    #0040   f8 d9
    def _prep_checksum(self):
        self.ip_checksum = [

        ]
    def _get_header_checksum(self):
        checksum = 0
        for i in range(0, len(self.ip_header), 2):
            checksum += int.from_bytes(self.ip_header[i], byteorder='big') + int.from_bytes(self.ip_header[i+1], byteorder='big')
            print(bin(checksum))