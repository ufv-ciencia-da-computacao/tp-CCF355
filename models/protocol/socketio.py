from ast import Break
from ..protocol.command import (
    Command,
    RequestAllUsersCommand,
    RequestAnswerTradeCommand,
    RequestLoginCommand,
    RequestCreateUserCommand,
    RequestTradeUserToUserCommand,
    ResponseCreateUserCommand,
)
import socket
import json

from models.domain import entity
from ..repository import repo


class Reader:
    def _read_message(sock: socket.socket):
        with sock:
            chunks = []
            print("reading_message")
            while True:
                try:
                    data = sock.recv(4096)
                    chunks.append(data.decode("utf-8"))
                except socket.timeout:
                    break
                if not data:
                    break

            return "".join(chunks)


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
                cmd = ResponseCreateUserCommand(False)
        elif message_type == RequestLoginCommand.__name__:
            pass
        elif message_type == RequestTradeUserToUserCommand.__name__:
            pass
        elif message_type == RequestAnswerTradeCommand.__name__:
            pass

        return cmd  # diferente


class ReaderResponse(Reader):
    def read(self, sock: socket.socket):
        data = Reader._read_message(sock)
        data = json.loads(data)
        message_type = data["message_type"]

        if message_type == ResponseCreateUserCommand.__name__:
            return data


class Writer:
    def _write_string(sock: socket.socket, msg: str) -> None:
        print(msg)
        sent = sock.sendall(msg.encode("utf-8"))
        if sent == 0:
            print("error")

    @staticmethod
    def write_command(sock: socket.socket, cmd: Command) -> str:
        return Writer._write_string(sock, cmd.execute())
