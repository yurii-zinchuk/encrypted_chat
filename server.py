"""Module for server script."""

import socket
import threading


class Server:
    def __init__(self, host, port) -> None:
        self.address = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def receive(self):
        while True:
            client, address = self.sock.accept()
            print(f"Connected with {str(address)}.")

            client.send("NICK".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")

            self.clients[client] = nickname

            print(f"Nickname of client: {nickname}")
            self.broadcast(f"{nickname} joined chat.\n".encode("utf-8"))
            client.send("Connected!".encode("utf-8"))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                decoded_msg = message.decode("utf-8")
                if decoded_msg == "Æ":
                    raise ConnectionAbortedError
                self.broadcast(message)
            except:
                self.clients.pop(client)
                break

    def run(self):
        self.sock.bind((self.address, self.port))
        self.sock.listen()
        print("Server running...")
        self.receive()


if __name__ == "__main__":
    server = Server("127.0.0.1", 9090)
    server.run()
