import socket
import struct
import time
# A class to create custom packet objects depending on the type of service
# being scanned. Can create custom packets as well as parse incoming packets.

class Packet():
    def __init__(self, src_port, port, src="127.0.0.1", dst="127.0.0.1"):
        self.src = src
        self.dst = socket.inet_aton(dst)
        self.dst_string = dst
        self.port = port

        # IP packet
        self.version =          0x4
        self.ihl =              0x5
        self.v_ihl =            (self.version << 4) + self.ihl
        self.tos =              0x0
        self.total_len =        0x28
        self.identification =   0xabcd
        self.flags = 0x0
        self.fragment_offset = 0x0
        self.f_fo = (self.flags << 13) + self.fragment_offset
        self.ttl =              0x40
        self.protocol =         0x6
        self.header_checksum =  0x0

        # TCP packet
        self.src_port =         src_port
        self.dst_port =         port
        self.seq_num =          0x0
        self.ack_num =          0x0
        self.data_offset =      0x5
        self.reserved =         0x0
        self.ns, self.cwr, self.ece, self.urg, self.ack, self.psh, self.rst, self.syn, self.fin =   0x0, 0x0, 0x0,\
                                                                                                    0x0, 0x0, 0x0,\
                                                                                                    0x0, 0x1, 0x0
        self.window_size =      0x7110
        self.tcp_checksum =     0x0
        self.urg_pointer =      0x0
        self.data_offset_res_flags =    (self.data_offset << 12) + (self.reserved << 9) + (self.ns << 8) + \
                                        (self.cwr << 7) + (self.ece << 6) + (self.urg << 5) + (self.ack) + \
                                        (self.psh << 3) + (self.rst << 2) + (self.syn << 1) + self.fin
        # packet
        self.tcp_header =   b""
        self.ip_header =    b""
        self.packet =       b""

        self._gen_packet()

    def _get_ip_checksum(self, data):
        check_sum = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i+1]
            check_sum += word
        check_sum = (check_sum >> 16) + (check_sum & 0xffff)
        check_sum = ~check_sum & 0xffff
        return check_sum

    def _gen_tcp_tmp_header(self):
        tmp_tcp_header = struct.pack("!HHLLHHHH", self.src_port, self.dst_port,
                                     self.seq_num, self.ack_num,
                                     self.data_offset_res_flags, self.window_size,
                                     self.tcp_checksum, self.urg_pointer)
        return tmp_tcp_header

    def _gen_ip_header(self):
        tmp_ip_header = struct.pack("!BBHHHBBH4s4s", self.v_ihl, self.tos, self.total_len,
                                    self.identification, self.f_fo, self.ttl, self.protocol,
                                    self.header_checksum, self.src, self.dst)
        return tmp_ip_header

    def _gen_packet(self):
        final_ip_header = struct.pack("!BBHHHBBH4s4s", self.v_ihl, self.tos, self.total_len,
                                                self.identification, self.f_fo,
                                                self.ttl, self.protocol, self._get_ip_checksum(self._gen_ip_header()),
                                                self.src,
                                                self.dst)
        tmp_tcp_header = self._gen_tcp_tmp_header()
        psuedo_tcp_header = struct.pack("!4s4sBBH", self.src, self.dst, self.tcp_checksum, self.protocol, len(tmp_tcp_header))
        tcp = tmp_tcp_header + psuedo_tcp_header
        final_tcp_header = struct.pack("!HHLLHHHH", self.src_port, self.dst_port, self.seq_num,
                                       self.ack_num, self.data_offset_res_flags, self.window_size,
                                       self._get_ip_checksum(tcp), self.urg_pointer)
        self.ip_header = final_ip_header
        self.tcp_header = final_tcp_header
        self.packet = final_ip_header + final_tcp_header

    
    def send_packet(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.sendto(self.packet, (self.dst_string, 0))
        time.sleep(0.2)
        data = s.recvfrom(1024)
        s.close()
        flags = data[0][33]
        return (flags == 18)
    
    def full_connection(self):
        HOST = self.dst_string  # The server's hostname or IP address
        PORT = self.dst_port  # The port used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((HOST, PORT))
        s.send(b"HEAD / HTTP/1.1\r\n\r\n")
        data = s.recv(1024).decode("utf-8", errors="ignore").strip()
        return data.split("\n")[0]
