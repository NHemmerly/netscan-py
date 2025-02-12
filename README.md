# netscan-py

## Overview

My plan for this project is to create a robust port scanning tool using Python. Taking clear inspiration from [nmap](https://nmap.org/). I chose to do this as my first personal project for my [boot.dev](https://www.boot.dev/tracks/backend) backend programming course. My goals for this project are to learn more about how packets are built and sent by applications, and to gain a little bit of insight into what is happening under the hood in tools like nmap. 

I'm deeply interested in information security, so this project felt like a logical choice. 
### Todo
 1. Scan ranges of IP addresses based on syntax input by user. (Kind of complete, does not do combinations of syntax, but will scan cidr ranges, comma selections in the final octet, and hyphenated ranges in the final octet)
 2. Add a cleaner output
 3. Figure out why it sometimes runs really slowly (parallelization?)
 4. Add more information to the cli tool with argparse
 5. 

## Usage

`sudo python3 src/main.py -r <ip or ip-range> -p <port or port-range>`

### Output
```
--------------------------------
| Host: xxx.xxx.xxx.xx1        |
--------------------------------
| port | state | version | etc |
--------------------------------
|  22  | OPEN  | v1.0    | WIP |

```



