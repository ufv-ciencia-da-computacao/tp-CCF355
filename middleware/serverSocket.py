import socket
import threading
import traceback
import sys

from models.protocol.socketio import ClientDisconnectedException, ReaderRequest
from models.repository.repo import (
    ListStickersRepository,
    StickersRepository,
    TradeRepository,
    TradeStickersRepository,
    UsersRepository,
)
from models.protocol.socketio import Writer


class ServerSocket:

    HOST = "127.0.0.1"
    PORT = 5555

    def __init__(
        self,
        us_repo: UsersRepository,
        s_repo: StickersRepository,
        ls_repo: ListStickersRepository,
        t_repo: TradeRepository,
        tr_repo: TradeStickersRepository,
    ) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))

        self.reader_request = ReaderRequest(us_repo, s_repo, ls_repo, t_repo, tr_repo)

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print(f"Connected by {address}")
            threading.Thread(target=self._start, args=(client,)).start()

    def _start(self, client):
        while True:
            try:
                cmd = self.reader_request.read(client)
                Writer.write_command(client, cmd)
            except ClientDisconnectedException:
                print("connection closed")
                client.close()
                return
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
