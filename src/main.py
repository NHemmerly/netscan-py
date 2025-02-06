import argparse
from scanner import Scanner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type")
    parser.add_argument("-p", "--ports")
    parser.add_argument("-r", "--range")
    args = parser.parse_args()
    scanny = Scanner(args.type, port=int(args.ports), range=args.range)

    scanny.scan()

if __name__ == "__main__":
    main()