import argparse
from scanner import Scanner

def main():
    print("Hello World!")
    parser = argparse.ArgumentParser()
    parser.add_argument("client_server")
    parser.add_argument("port")
    args = parser.parse_args()
    scanny = Scanner(args.client_server, port=int(args.port))

    scanny.scan()

if __name__ == "__main__":
    main()