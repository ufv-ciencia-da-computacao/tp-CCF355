import socket
from models.protocol.socketio import ReaderResponse, Writer


class ClientSocket:
    HOST = "127.0.0.1"
    PORT = 5555

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send_receive(self, command):

        with self.sock as s:
            self.sock.connect((self.HOST, self.PORT))
            self.sock.settimeout(5)
            Writer.write_command(s, command)
            data = ReaderResponse().read(s)
            return data
