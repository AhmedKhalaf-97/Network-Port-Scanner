import sys
from socket import *


def create_TCP_server(server_port):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", server_port))
    serverSocket.listen(1)

    print("The TCP server is ready to receive on port:", server_port)
    while True:
        connectionSocket, addr = serverSocket.accept()
        msg = connectionSocket.recv(2048).decode()


def create_UDP_server(server_port):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(("0.0.0.0", server_port))

    print("The UDP server is ready to receive on port:", server_port)
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        print(" A message received by the server. The message is: ", message.decode())
        resp = "PONG"
        if message.decode() == "message":
            serverSocket.sendto(resp.encode(), clientAddress)
        else:
            print("No  message received")


def main():
    if len(sys.argv) != 3:
        print(" Usage: python server.py <protocol> <port number>")
        sys.exit(1)
    else:
        protocol = str(sys.argv[1])
        server_port = int(sys.argv[2])
        if protocol.upper() == "TCP":
            create_TCP_server(server_port)
        elif protocol.upper() == "UDP":
            create_UDP_server(server_port)


if __name__ == "__main__":
    main()
