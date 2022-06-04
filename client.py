"""Module for client script."""

import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import encryption.rsa as rsa


class Client:
    def __init__(self, host, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.gui_done = False
        self.running = True

    def run(self):
        (n, e), d = rsa.generate_keys()
        self.public, self.secret = (n, e), d

        # receive server public key
        server_public = tuple(
            map(lambda x: int(x), self.sock.recv(1024).decode().split("|"))
        )

        # send self keys to server
        keys_str = (
            (str(n)) + "|" + str(e) + "|" + rsa.rsa_encrypt(str(d), server_public)
        )
        self.sock.send(keys_str.encode())

        msg = tkinter.Tk()
        msg.withdraw()
        self.nick = simpledialog.askstring("Nick", "Choose nick", parent=msg)

        gui_thread = threading.Thread(target=self.gui_create)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    def gui_create(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.quit_button = tkinter.Button(self.win, text="Quit", command=self.stop)
        self.quit_button.config(font=("Arial", 12))
        self.quit_button.pack()

        self.chat_label = tkinter.Label(
            self.win, text=f"{self.nick}. Chat:", bg="lightgray"
        )
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack()

        self.win.bind("<Return>", self.write)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def stop(self):
        self.running = False
        self.sock.send("Æ".encode("utf-8"))
        self.win.destroy()
        self.sock.close()
        exit(0)

    def write(self, e=None):
        message = f"{self.nick}: {self.input_area.get('1.0', 'end')}".strip("\n")
        self.sock.send(rsa.rsa_encrypt(message, self.public).encode("utf-8"))
        self.input_area.delete("1.0", "end")

    def receive(self):
        # картинку просто прийняти і зберегти в папку
        while self.running:
            try:
                message = rsa.rsa_decrypt(
                    self.sock.recv(1024).decode("utf-8"), self.secret, self.public
                )
                if message == "NICK":
                    encr_nick = rsa.rsa_encrypt(self.nick, self.public)
                    self.sock.send(encr_nick.encode("utf-8"))
                else:
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert("end", message + "\n")
                        self.text_area.yview("end")
                        self.text_area.config(state="disabled")
            except ConnectionAbortedError:
                break
            except Exception as err:
                print(err)
                break


if __name__ == "__main__":
    client = Client("127.0.0.1", 9090)
    client.run()
