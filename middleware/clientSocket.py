import socket
from models.protocol.socketio import ReaderResponse, Writer


class ClientSocket:
    HOST = "127.0.0.1"
    PORT = 5555

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def send_receive(self, command):
        self.sock.connect((self.HOST, self.PORT))
        Writer.write_command(self.sock, command)
        data = ReaderResponse().read(self.sock)
        self.sock.close()
        return data
