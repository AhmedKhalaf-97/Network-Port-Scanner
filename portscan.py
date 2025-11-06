# Name: Ahmed Khalaf
# Course: CSC138 Computer Network Fundamentals - SECTION 01
# Date: 11/06/2025

# Description:
# This program implements a simple network port scanner that reports
# the status of TCP and UDP ports for a given host within a user-defined
# port range. It determines whether each port is open or closed using
# socket connections and identifies the service name (when available).

# The program accepts four command-line arguments:
#   python3 portscan.py <hostname> <protocol> <portlow> <porthigh>


# Import system and socket modules.
import sys
from socket import *


# Function that scans a single TCP port. Accepts the hostname and the port.
def port_scan_TCP(hostname, port):
    # Try/Except block in case the socket times out or throws any exception.
    try:
        # Open a TCP socket.
        scanner_socket = socket(AF_INET, SOCK_STREAM)
        # Set timeout of 1 second.
        scanner_socket.settimeout(1)
        # Attempt to connect to the port.
        connection_status = scanner_socket.connect_ex((hostname, port))
        # If the connection is successful or if the port is open, the connection status will be 0, otherwise, it's closed.
        if connection_status == 0:
            # Get the service name running on the port.
            try:
                port_service_name = getservbyport(port, "tcp")
            except Exception as e:
                # OSError: in case the service name is not available.
                port_service_name = "svc name unavail"
            print("port", port, "open   :", port_service_name)
        else:
            print("port", port, "closed")
    except Exception as e:
        # timeout: in case the connections times out.
        print("port", port, "closed")
    finally:
        # After scanning, close the socket.
        scanner_socket.close()


# Function that scans a single UDP port. Accepts the hostname and the port.
def port_scan_UDP(hostname, port):
    # Try/Except block in case the socket times out or throws any exception.
    try:
        # Open a UDP socket.
        scanner_socket = socket(AF_INET, SOCK_DGRAM)
        # Set timeout of 1 second.
        scanner_socket.settimeout(1)
        # Attempt to send a query message to the port.
        scanner_socket.sendto("message".encode(), (hostname, port))
        # If it recieves a response back, that means the UDP port is open.
        pongMsg, server_address = scanner_socket.recvfrom(2048)
        # Check the response back.
        if pongMsg.decode() == "PONG":
            # Get the service name running on the port.
            try:
                port_service_name = getservbyport(port, "udp")
            except Exception as e:
                # OSError: in case the service name is not available.
                port_service_name = "svc name unavail"
            print("port", port, "open   :", port_service_name)
        else:
            print("port", port, "closed")
    except Exception as e:
        # timeout: in case the connections times out.
        print("port", port, "closed")
    finally:
        # After scanning, close the socket.
        scanner_socket.close()


# Function that runs port scanner based on the specified protocol.
def port_scanner(hostname, protocol, portlow, porthigh):
    # Go through the ports, and scan them individually.
    for port in range(portlow, porthigh + 1):
        # It will scan the ports based on the specified protocol.
        if protocol == "TCP":
            port_scan_TCP(hostname, port)

        elif protocol == "UDP":
            port_scan_UDP(hostname, port)


# Function that checks the validity of the hostname.
def check_hostname(hostname):
    try:
        gethostbyname(hostname)
        return True
    except gaierror as e:
        return False


# The main entry point of the program.
def main(argv):
    # The program will accept 4 command-line arguments
    if len(sys.argv) == 5:
        try:
            hostname = str(sys.argv[1])
            protocol = str(sys.argv[2])
            portlow = int(sys.argv[3])
            porthigh = int(sys.argv[4])

            # Checks if the inputted hostname is valid.
            if check_hostname(hostname) == False:
                print(
                    f"scanning host={hostname}, protocol={protocol}, ports: {portlow} -> {porthigh} error: host {hostname} does not exist"
                )
                sys.exit(1)

            # Call the port scanner with the inputted values from the user.
            if protocol.upper() == "TCP":
                port_scanner(hostname, "TCP", portlow, porthigh)
            elif protocol.upper() == "UDP":
                port_scanner(hostname, "UDP", portlow, porthigh)
            else:
                # The program will terminate if incorrect protocol.
                print(
                    f'scanning host={hostname}, protocol={protocol}, ports: {portlow} -> {porthigh} invalid protocol: {protocol}. Specify "tcp" or "udp"'
                )
                sys.exit(1)

        except ValueError:
            # The program will terminate if inputted ports are not integer type.
            print(
                "Invalid port input.\nUsage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>"
            )
    else:
        # The program will terminate if it there is anything else other than 4 arguments.
        print("Usage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
