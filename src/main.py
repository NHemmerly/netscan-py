import argparse
import asyncio
from scanner import Scanner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type")
    parser.add_argument("-p", "--ports")
    parser.add_argument("-r", "--range")
    args = parser.parse_args()
    scanny = Scanner(args.type, port=args.ports, range=args.range)
    asyncio.run(scanny.async_scan())

if __name__ == "__main__":
    main()