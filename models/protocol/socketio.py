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

EOF = 0x05


class Reader:
    def _read_message(sock: socket.socket):
        chunks = []
        print("address: ", sock.getsockname())

        while True:
            data = sock.recv(4096)
            for d in data:
                if d == EOF:
                    return "".join(chunks)
                chunks.append(str(bytearray([d]).decode("utf-8")))
            if not data:
                print("communication failed")
                break

        return ""


class ReaderRequest(Reader):
    def __init__(self, us_repo: repo.UsersRepository) -> None:
        self.us_repo = us_repo

    def read(self, sock: socket.socket):
        data = Reader._read_message(sock)
        data = json.loads(data)
        message_type = data["message_type"]

        if message_type == RequestCreateUserCommand.__name__:
            u = entity.Users(username=data["username"], password=data["password"])
            try:
                self.us_repo.add(u)
                cmd = ResponseCreateUserCommand(True)
            except Exception:
                traceback.print_exception(*sys.exc_info())
                cmd = ResponseCreateUserCommand(False)
        elif message_type == RequestLoginCommand.__name__:
            login_cmd = RequestLoginCommand.from_dict(data)
            list_users = self.us_repo.list()
            cmd = ResponseLoginCommand(entity.Users("",""))
            for user in list_users:
                if user.username == login_cmd.username and user.password == login_cmd.password:
                    cmd = ResponseLoginCommand(user=user)
        elif message_type == RequestTradeUserToUserCommand.__name__:
            pass
        elif message_type == RequestAnswerTradeCommand.__name__:
            pass

        return cmd


class ReaderResponse(Reader):
    @staticmethod
    def read(sock: socket.socket):
        data = Reader._read_message(sock)
        data = json.loads(data)
        cmd = None
        if data["message_type"] == ResponseCreateUserCommand.__name__:
            cmd = ResponseCreateUserCommand.from_dict(data)
        elif data["message_type"] == ResponseLoginCommand.__name__:
            cmd = ResponseLoginCommand.from_dict(data)

        return cmd


class Writer:
    def _write_string(sock: socket.socket, msg: str) -> None:
        print(msg)
        sock.sendall(msg.encode("utf-8"))
        sock.sendall(bytearray([EOF]))

    @staticmethod
    def write_command(sock: socket.socket, cmd: Command) -> str:
        return Writer._write_string(sock, cmd.execute())
