from ast import Break
from ..protocol.command import (
    Command,
    RequestAllUsersCommand,
    RequestAnswerTradeCommand,
    RequestLoginCommand,
    RequestCreateUserCommand,
    RequestTradeUserToUserCommand,
    ResponseCreateUserCommand,
    ResponseLoginCommand,
)
import socket
import json
import traceback
import sys

from models.domain import entity
from ..repository import repo
from ..service.StickersPack import StickersPack

EOF = 0x05


class Reader:
    def _read_message(sock: socket.socket):
        chunks = []
        print("address: ", sock.getsockname())

        while True:
            data = sock.recv(4096)
            if data[len(data) - 1] == EOF:
                decode = data[: len(data) - 1].decode("utf-8")
                return decode
            else:
                chunks.append(str(data.decode("utf-8")))
            if not data:
                print("communication failed")
                break

        return "".join(chunks)


class ReaderRequest(Reader):
    def __init__(
        self,
        us_repo: repo.UsersRepository,
        s_repo: repo.StickersRepository,
        ls_repo: repo.ListStickersRepository,
    ) -> None:
        self.us_repo = us_repo
        self.s_repo = s_repo
        self.ls_repo = ls_repo
        self.stickerspack = StickersPack(s_repo, ls_repo)

    def read(self, sock: socket.socket):
        data = Reader._read_message(sock)
        data = json.loads(data)
        message_type = data["message_type"]

        if message_type == RequestCreateUserCommand.__name__:
            u = entity.Users(username=data["username"], password=data["password"])
            try:
                self.us_repo.add(u)
                cmd = ResponseCreateUserCommand(True)
                for _ in range(5):
                    self.stickerspack.add_pack2user(user=self.us_repo.get(u.username))
            except Exception:
                traceback.print_exception(*sys.exc_info())
                cmd = ResponseCreateUserCommand(False)

        elif message_type == RequestLoginCommand.__name__:
            try:
                user = self.us_repo.get(data["username"])

                if user is not None:
                    cmd = ResponseLoginCommand(user=user)
                else:
                    cmd = ResponseLoginCommand(entity.Users("", ""))
            except:
                traceback.print_exception(*sys.exc_info())
                # cmd = ErrorCommand()

        elif message_type == RequestTradeUserToUserCommand.__name__:
            pass
        elif message_type == RequestAnswerTradeCommand.__name__:
            pass

        return cmd


class ReaderResponse(Reader):
    @staticmethod
    def read(sock: socket.socket):
        data = Reader._read_message(sock)
        print(data)
        data = json.loads(data)
        cmd = None
        if data["message_type"] == ResponseCreateUserCommand.__name__:
            cmd = ResponseCreateUserCommand.from_dict(data)
        elif data["message_type"] == ResponseLoginCommand.__name__:
            cmd = ResponseLoginCommand.from_dict(data)

        return cmd


class Writer:
    def _write_string(sock: socket.socket, msg: str) -> None:
        print(len(msg))
        sock.sendall(msg.encode("utf-8"))
        sock.sendall(bytearray([EOF]))

    @staticmethod
    def write_command(sock: socket.socket, cmd: Command) -> str:
        return Writer._write_string(sock, cmd.execute())
