"""Module for server script."""

import socket
import threading

HOST = "127.0.0.1"
PORT = 9090


class Server:
    def __init__(self, host, port) -> None:
        self.address = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicks = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def receive(self):
        while True:
            client, address = self.sock.accept()
            print(f"Connected with {str(address)}.")

            client.send("NICK".encode("utf-8"))
            nickname = client.recv(1024)

            self.nicks.append(nickname)
            self.clients.append(client)

            print(f"Nickname of client: {nickname}")
            self.broadcast(f"{nickname} joined chat.\n".encode("utf-8"))
            client.send("Connected!".encode("utf-8"))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                print(f"{self.nicks[self.clients.index(client)]}")
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicks[index]
                self.nicks.remove(nickname)
                break

    def run(self):
        self.sock.bind((self.address, self.port))
        self.sock.listen()
        print("Server run...")
        self.receive()


if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.run()
