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
        session
    ) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))

        self.session = session

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            print(f"Connected by {address}")
            threading.Thread(target=self._start, args=(client,self.session(),)).start()

    def _start(self, client, session):
        s_repo = StickersRepository(session)
        ls_repo = ListStickersRepository(session)
        us_repo = UsersRepository(session)
        t_repo = TradeRepository(session)
        tr_repo = TradeStickersRepository(session)

        reader_request = ReaderRequest(us_repo, s_repo, ls_repo, t_repo, tr_repo)
        
        while True:
            try:
                cmd = reader_request.read(client)
                Writer.write_command(client, cmd)
            except ClientDisconnectedException:
                print("connection closed")
                client.close()
                return
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
