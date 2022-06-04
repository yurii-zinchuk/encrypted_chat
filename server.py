"""Module for server script."""

import socket
import threading
from client import Client
import encryption.rsa as rsa


class Server:
    """
    A class to represent server.
    """

    def __init__(self, host: str, port: int) -> None:
        """Define server object.

        Args:
            host (str): IP address of host.
            port (int): Port of connection.
        """
        self.address = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}

    def broadcast(self, message: str) -> None:
        """Send message to all users in the chat,
        encode it with their key.

        Args:
            message (str): Message to send.
        """
        for client in self.clients:
            client.send(
                rsa.rsa_encrypt(message, self.clients[client][1][0]).encode("utf-8")
            )

    def receive(self) -> None:
        """Receive connections from users, exchange keys."""
        # create keys
        (n, e), d = rsa.generate_keys()
        self.public, self.secret = (n, e), d
        public_str = str(n) + "|" + str(e)

        while True:
            client, address = self.sock.accept()
            print(f"Connected with {str(address)}.")

            # send self public to client
            client.send(public_str.encode())

            # get encoded client keys
            n, e, d = client.recv(1024).decode().split("|")

            cli_public = int(n), int(e)
            cli_secret = int(rsa.rsa_decrypt(d, self.secret, self.public))

            client.send(rsa.rsa_encrypt("NICK", cli_public).encode("utf-8"))
            nickname = rsa.rsa_decrypt(
                client.recv(1024).decode("utf-8"), cli_secret, cli_public
            )

            self.clients[client] = nickname, (cli_public, cli_secret)

            print(f"Nickname of client: {nickname}")
            self.broadcast(f"{nickname} joined chat.")

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def handle(self, client: Client):
        """Main server loop.
        Receive and send messages between users.

        Args:
            client (Client): Client that sent the message.

        Raises:
            ConnectionAbortedError: If client left chat.
        """
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if message == "Æ":
                    raise ConnectionAbortedError

                message = rsa.rsa_decrypt(
                    message, self.clients[client][1][1], self.clients[client][1][0]
                )
                self.broadcast(message)
            except:
                self.clients.pop(client)
                break

    def run(self) -> None:
        """Initialize and run server script."""
        self.sock.bind((self.address, self.port))
        self.sock.listen()
        print("Server running...")
        self.receive()


if __name__ == "__main__":
    server = Server("127.0.0.1", 9090)
    server.run()
