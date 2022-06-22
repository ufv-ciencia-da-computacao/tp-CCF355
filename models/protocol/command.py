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


class TradeUserToUserCommand(Command):  # serialize object
    def __init__(
        self,
        user_orig: int,
        stickers_user_orig: list,
        user_dest: int,
        stickers_user_dest: list,
    ):
        self.message_type = TradeUserToUserCommand.__name__
        self.user_orig = user_orig
        self.user_dest = user_dest
        self.stickers_user_orig = stickers_user_orig
        self.stickers_user_dest = stickers_user_dest

    def as_dict(self):
        return self.__dict__


class AcceptTradeCommand(Command):
    def as_dict(self):
        pass


class RecusedTradeCommand(Command):
    def as_dict(self):
        pass


class RequestCreateLoginCommand(Command):
    def __init__(self, name: str, password: str) -> None:
        self.name = name
        self.password = password
        self.message_type = RequestCreateLoginCommand.__name__

    def as_dict(self):
        return {"name": self.name, "password": self.password}


class RequestListUserStickersCommand(Command):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.message_type = RequestListUserStickersCommand.__name__

    def as_dict(self):
        return {"user_id": self.user_id, "message_type": self.message_type}


class ResponseListStickersCommand(Command):
    def __init__(self, stickers: List[entity.Stickers]) -> None:
        self.stickers = stickers
        self.message_type = ResponseListStickersCommand.__name__

    def as_dict(self):
        return {
            "stickers": [s.as_dict() for s in self.stickers],
            "message_type": self.message_type,
        }
