# Network-Port-Scanner
This is an assignment for a class: CSC138 Computer Network Fundamentals.
# Network Port Scanner

A command-line network port scanner written in Python. This program scans a given host over a specified range of ports and reports whether each port is open or closed for either TCP or UDP.

The scanner also attempts to identify the service running on open ports when service information is available.

## Features

* Scan a remote host by hostname
* Supports both TCP and UDP scanning
* Accepts a custom port range
* Displays whether each port is open or closed
* Attempts to identify common services by port number
* Uses socket timeouts to prevent the program from hanging
* Handles invalid hosts, invalid protocols, and missing arguments

## Technologies Used

* Python 3
* Python `socket` library
* TCP sockets using `SOCK_STREAM`
* UDP sockets using `SOCK_DGRAM`

## How It Works

The scanner takes a hostname, protocol, and port range as command-line arguments.

For TCP scans, the program attempts to connect to each port using `connect_ex()`. If the connection succeeds, the port is reported as open. Otherwise, it is reported as closed.

For UDP scans, the program sends a test message to the target port and waits for a response. If a response is received before the timeout, the port is considered open. If no response is received, the service is treated as unavailable.

When a port is open, the program uses `socket.getservbyport()` to attempt to identify the service name. If the service name cannot be found, it displays:

```text
svc name unavail
```

## Usage

```bash
python3 portscan.py <hostname> <protocol> <portlow> <porthigh>
```

### Arguments

| Argument     | Description                         |
| ------------ | ----------------------------------- |
| `<hostname>` | The hostname of the machine to scan |
| `<protocol>` | The protocol to use: `tcp` or `udp` |
| `<portlow>`  | The starting port number, inclusive |
| `<porthigh>` | The ending port number, inclusive   |

## Example Commands

Scan TCP port 22:

```bash
python3 portscan.py ecs-coding1.csus.edu tcp 22 22
```

Scan a range of TCP ports:

```bash
python3 portscan.py ecs-coding1.csus.edu tcp 20 30
```

Scan a UDP port:

```bash
python3 portscan.py ecs-coding1.csus.edu udp 8001 8001
```

## Example Output

```text
scanning host=ecs-coding1.csus.edu, protocol=tcp, ports: 20 -> 30
port 20 closed
port 21 closed
port 22 open : ssh
port 23 closed
port 24 closed
port 25 closed
port 26 closed
port 27 closed
port 28 closed
port 29 closed
port 30 closed
```

## Error Handling

The program checks for common errors, including:

* Missing command-line arguments
* Invalid protocol input
* Invalid or unreachable hostname
* Socket timeouts
* Connection errors

If the user does not provide all required arguments, the program displays a usage message:

```text
usage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>
```

## File Structure

```text
.
├── portscan.py
└── README.md
```

## Requirements

* Python 3 installed
* Network access to the target host
* Permission to scan the target machine

## Important Note

This project is intended for educational purposes only. Only scan machines that you own or have permission to test. Unauthorized port scanning may violate network policies or laws.
