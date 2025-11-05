import sys
import threading
from socket import *


def port_scan_TCP_task(hostname, port):
    try:
        scanner_socket = socket(AF_INET, SOCK_STREAM)
        scanner_socket.settimeout(1)
        connection_status = scanner_socket.connect_ex((hostname, port))
        if connection_status == 0:
            try:
                port_service_name = socket.getservbyport(port, "tcp")
            except Exception as e:
                # OSError
                port_service_name = "svc name unavail"
            print("port", port, "open   :", port_service_name)
        else:
            print("port", port, "closed")
    except Exception as e:
        # timeout
        print("port", port, "closed")
    finally:
        scanner_socket.close()


def port_scan_UDP_task(hostname, port):
    try:
        scanner_socket = socket(AF_INET, SOCK_DGRAM)
        scanner_socket.settimeout(1)

        scanner_socket.sendto("message".encode(), (hostname, port))
        pongMsg, server_address = scanner_socket.recvfrom(2048)

        if pongMsg.decode() == "PONG":
            try:
                port_service_name = socket.getservbyport(port, "udp")
            except Exception as e:
                # OSError
                port_service_name = "svc name unavail"
            print("port", port, "open   :", port_service_name)
        else:
            print("port", port, "closed")
    except Exception as e:
        # timeout
        print("port", port, "closed")
    finally:
        scanner_socket.close()


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


def check_hostname(hostname):
    try:
        gethostbyname(hostname)
        return True
    except gaierror as e:
        return False


def main(argv):
    # The program will accept command-line arguments:
    if len(sys.argv) == 5:
        try:
            hostname = str(sys.argv[1])
            protocol = str(sys.argv[2])
            portlow = int(sys.argv[3])
            porthigh = int(sys.argv[4])

            if check_hostname(hostname) == False:
                print(
                    f"scanning host={hostname}, protocol={protocol}, ports: {portlow} -> {porthigh} error: host {hostname} does not exist"
                )
                sys.exit(1)

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
            print(
                "Invalid port input.\nUsage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>"
            )
    else:
        # The program will terminate if it there is anything else other than 4 arguments.
        print("Usage: python3 portscan.py <hostname> <protocol> <portlow> <porthigh>")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
