import command
import socket
import json

from models.domain import entity
from ..repository import repo


class Reader:
    def _read_message(sock: socket.socket):
        chunks = []
        bytes_recd = 0
        while bytes_recd < 2048:
            chunk = sock.recv(min(2048 - bytes_recd, 2048))
            if chunk == b"":
                print("error")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b"".join(chunks)


class ReaderRequest(Reader):
    def __init__(self, us_repo: repo.UsersRepository) -> None:
        self.us_repo = us_repo

    def read(self, sock: socket.socket):
        data = self.read_message(sock)
        data = json.loads(data)
        message_type = data["message_type"]

        if message_type == command.RequestCreateUserCommand.__name__:
            u = entity.Users(username=data["username"], password=data["password"])
            self.us_repo.add(u)
            Writer.write_command(command.ResponseCreateUserCommand)
        elif message_type == command.RequestTradeUserToUserCommand.__name__:
            pass
        elif message_type == command.RequestAnswerTradeCommand.__name__:
            pass


class Writer:
    def _write_string(sock: socket.socket, msg: str) -> None:
        total_sent = 0
        while total_sent < 2048:
            sent = sock.send(msg[total_sent:])
            if sent == 0:
                print("error")
            total_sent += sent

    @staticmethod
    def write_command(cmd: command.Command) -> str:
        return Writer._write_string(cmd.execute())
