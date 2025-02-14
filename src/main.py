import argparse
from scanner import Scanner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--ports", help="Define the port or range of ports you intend to scan ex. 22, 135-139, 443")
    parser.add_argument("-r", "--range", help="Define the ip or range/CIDR range of addresses to scan ex. 192.168.1.20, 192.168.1.25-35, 192.168.2.0/24")
    parser.add_argument("-v", "--version", help="*WIP* Set to True to enable version scanning", default="false")
    args = parser.parse_args()
    scanny = Scanner(port=args.ports, range=args.range, version=args.version)
    scanny.scan()

if __name__ == "__main__":
    main()