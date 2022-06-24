import json
from typing import List

from ..domain import entity


class Command:

    message_type: str

    def execute(self):
        return json.dumps(self.as_dict(), ensure_ascii=False)

    def as_dict(self):
        return self.__dict__


class RequestTradeUserToUserCommand(Command):  # serialize object
    def __init__(
        self,
        user_orig: int,
        stickers_user_orig: list,
        user_dest: int,
        stickers_user_dest: list,
    ):
        self.message_type = RequestTradeUserToUserCommand.__name__
        self.user_orig = user_orig
        self.user_dest = user_dest
        self.stickers_user_orig = stickers_user_orig
        self.stickers_user_dest = stickers_user_dest


class ResponseTradeUserToUserCommand(Command):
    def __init__(self, trade: entity.TradeRequest):
        self.message_type = ResponseTradeUserToUserCommand.__name__
        self.trade = trade


class RequestAnswerTradeCommand(Command):
    def __init__(self, accept: bool):
        self.message_type = RequestAnswerTradeCommand.__name__
        self.accept = accept


class ResponseAnswerTradeCommand(Command):
    def __init__(self, status: bool):
        self.message_type = ResponseAnswerTradeCommand.__name__
        self.status = status


class RequestCreateUserCommand(Command):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.message_type = RequestCreateUserCommand.__name__


class ResponseCreateUserCommand(Command):
    def __init__(self, status: bool):
        self.message_type = ResponseCreateUserCommand.__name__
        self.status = status

    @staticmethod
    def from_dict(obj: dict):
        return ResponseCreateUserCommand(status=obj["status"])


class RequestLoginCommand(Command):
    def __init__(self, username: str, password: str):
        self.message_type = RequestLoginCommand.__name__
        self.username = username
        self.password = password

    @staticmethod
    def from_dict(obj: dict):
        return RequestLoginCommand(username=obj["username"], password=obj["password"])

class ResponseLoginCommand(Command):
    def __init__(self, user: entity.Users):
        self.message_type = ResponseLoginCommand.__name__
        self.user = user

    @staticmethod
    def from_dict(obj: dict):
        return ResponseLoginCommand(entity.Users.from_dict(obj["user"]))

    def as_dict(self):
        return {
            "message_type": ResponseLoginCommand.__name__,
            "user": self.user.as_dict()
        }


class RequestAllUsersCommand(Command):
    def __init__(self) -> None:
        self.message_type = RequestAllUsersCommand.__name__


class ResponseAllUsersCommand(Command):
    def __init__(self, users: List[entity.Users]):
        self.users = users
        self.message_type = ResponseAllUsersCommand.__name__

    def as_dict(self):
        return {
            "users": [u.as_dict() for u in self.users],
            "message_type": self.message_type,
        }
