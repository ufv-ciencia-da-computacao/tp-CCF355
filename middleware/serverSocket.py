import socket
import threading
import traceback
import sys

from models.protocol.socketio import ReaderRequest
from models.repository.repo import UsersRepository


class ServerSocket:

    HOST = "127.0.0.1"
    PORT = 5555

    def __init__(self, us_repo: UsersRepository) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))

        self.reader_request = ReaderRequest(us_repo)

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print(f"Connected by {address}")
            client.settimeout(60)
            threading.Thread(target=self._start, args=(client,)).start()

    def _start(self, client):
        while True:
            try:
                self.reader_request.read(client)
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
                client.close()
                return False
