import socket

class Scanner():
    def __init__(self, client_server,protocol=None, range="127.0.0.1", port=65432):
        self.range = range              # IP or CIDR IP range
        self.protocol = protocol        # TCP or UDP - most scans will be TCP 
        self.port = port                # Port or port range
        self.client_server = client_server


    def _determine_range(self):
        # Function for parsing ip range into a list of IPs to scan
        pass

    def _determine_ports(self):
        # function for parsing port input into a list of ports to scan
        pass

    def scan(self):
        if self.client_server == "client":
            self._client()
        elif self.client_server == "server":
            self._server()
        else:
            print("Invalid client_server arg")

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
        HOST = self.range  # The server's hostname or IP address
        PORT = self.port  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b"Hello, world")
            data = s.recv(1024)

        print(f"Received {data!r}")     