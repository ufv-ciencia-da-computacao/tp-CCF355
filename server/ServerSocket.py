from email.headerregistry import Address
import socket


class ServerSocket:

    HOST = "127.0.0.1"
    PORT = 3555

    addresses = []  # Turn to class

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        with self.sock as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            if addr not in self.addresses:
                self.addresses.append(addr)

            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
