import socket


class ClientSocket:
    HOST = "127.0.0.1"
    PORT = 3555

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        with self.sock as s:
            s.connect((self.HOST, self.PORT))
            data = s.recv(1024)
