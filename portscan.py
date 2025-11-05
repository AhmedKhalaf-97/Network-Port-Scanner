import sys
import threading
from socket import *


def port_scan_TCP_task(hostname, port):
    try:
        scanner_socket = socket(AF_INET, SOCK_STREAM)
        scanner_socket.settimeout(1)
        connection_status = scanner_socket.connect_ex((hostname, port))
        print(connection_status)
    except Exception as e:
        print("Failed to connect" + port)
    finally:
        scanner_socket.close()


def port_scan_UDP_task(hostname, port):
    print("Scanning UDP port: ", port)


def port_scanner(hostname, protocol, portlow, porthigh):
    scanner_threads = list()
    for port in range(portlow, porthigh + 1):
        if protocol == "TCP":
            scanner_t = threading.Thread(
                target=port_scan_TCP_task,
                args=(
                    hostname,
                    port,
                ),
            )
        elif protocol == "UDP":
            scanner_t = threading.Thread(
                target=port_scan_UDP_task,
                args=(
                    hostname,
                    port,
                ),
            )

        scanner_threads.append(scanner_t)
        scanner_t.start()

    for scanner_t in scanner_threads:
        scanner_t.join()


def main(argv):
    # The program will accept command-line arguments:
    if len(sys.argv) == 5:
        try:
            hostname = str(sys.argv[1])
            protocol = str(sys.argv[2])
            portlow = int(sys.argv[3])
            porthigh = int(sys.argv[4])

            if protocol.upper() == "TCP":
                port_scanner(hostname, "TCP", portlow, porthigh)
            elif protocol.upper() == "UDP":
                port_scanner(hostname, "UDP", portlow, porthigh)
            else:
                # The program will terminate if incorrect protocol.
                print(
                    "Usage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>"
                )
                sys.exit(1)

        except ValueError:
            print(
                "Invalid input. Please enter valid inputs.\nUsage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>"
            )
    else:
        # The program will terminate if it there is anything else other than 4 arguments.
        print("Usage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
