import socket
import threading

from models.protocol.socketio import ReaderRequest
from models.repository.repo import UsersRepository


class ServerSocket:

    HOST = "127.0.0.1"
    PORT = 8000

    def __init__(self, us_repo: UsersRepository) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        self.reader_request = ReaderRequest(us_repo)

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.start, args=(client)).start()

    def start(self, client):
        while True:
            try:
                self.reader_request.read(client)
            except:
                client.close()
                return False
