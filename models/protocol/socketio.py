import command
import socket
import json

from models.domain import entity
from ..repository import repo


class Reader:
    def _read_message(sock: socket.socket):
        with sock:
            chunks = []
            while True:
                try:
                    data = sock.recv(4096)
                except socket.timeout:
                    continue
                if not data:
                    break
                chunks.append(data)


class ReaderRequest(Reader):
    def __init__(self, us_repo: repo.UsersRepository) -> None:
        self.us_repo = us_repo

    def read(self, sock: socket.socket):
        data = self.read_message(sock)
        data = json.loads(data)
        message_type = data["message_type"]

        if message_type == command.RequestCreateUserCommand.__name__:
            u = entity.Users(username=data["username"], password=data["password"])
            try:
                self.us_repo.add(u)
                cmd = command.ResponseCreateUserCommand(True)
            except Exception as e:
                cmd = command.ResponseCreateUserCommand(False)
            Writer.write_command(sock, cmd)
        elif message_type == command.RequestTradeUserToUserCommand.__name__:
            pass
        elif message_type == command.RequestAnswerTradeCommand.__name__:
            pass


class ReaderResponse(Reader):
    def read(self, sock: socket.socket):
        data = self.read_message(sock)
        data = json.loads(data)
        message_type = data["message_type"]

        if message_type == command.ResponseCreateUserCommand.__name__:
            return data


class Writer:
    def _write_string(sock: socket.socket, msg: str) -> None:
        sent = sock.sendall(msg)
        if sent == 0:
            print("error")

    @staticmethod
    def write_command(sock: socket.socket, cmd: command.Command) -> str:
        return Writer._write_string(sock, cmd.execute())
