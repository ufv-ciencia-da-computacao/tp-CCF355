from abc import (
    ABC,
    abstractmethod,
)
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
    def __init__(self, name: str, password: str) -> None:
        self.name = name
        self.password = password
        self.message_type = RequestCreateUserCommand.__name__

class ResponseCreateUserCommand(Command):
    def __init__(self, user: entity.Users):
        self.message_type = ResponseCreateUserCommand.__name__
        self.user = user

class RequestLoginCommand(Command):
    def __init__(self, username: str, password: str):
        self.message_type = RequestLoginCommand.__name__
        self.username = username
        self.password = password

class ResponseLoginCommand(Command):
    def __init__(self, user: entity.Users):
        self.message_type = RequestLoginCommand.__name__
        self.user = user

class RequestListUserStickersCommand(Command):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.message_type = RequestListUserStickersCommand.__name__


class ResponseListStickersCommand(Command):
    def __init__(self, stickers: List[entity.Stickers]):
        self.stickers = stickers
        self.message_type = ResponseListStickersCommand.__name__

    def as_dict(self):
        return {
            "stickers": [s.as_dict() for s in self.stickers],
            "message_type": self.message_type,
        }
