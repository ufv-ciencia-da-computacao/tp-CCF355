import json
from typing import List

from models.domain.entity import Status, Stickers
from ..domain import entity


class Command:

    message_type: str

    def execute(self):
        return json.dumps(self.as_dict(), ensure_ascii=False)

    def as_dict(self):
        return self.__dict__


class RequestTradeUserToUserCommand(Command):
    def __init__(
        self,
        user_orig: str,
        stickers_user_orig: List[int],
        user_dest: str,
        stickers_user_dest: List[int],
    ):
        self.message_type = RequestTradeUserToUserCommand.__name__
        self.user_orig = user_orig
        self.user_dest = user_dest
        self.stickers_user_orig = stickers_user_orig
        self.stickers_user_dest = stickers_user_dest


class ResponseTradeUserToUserCommand(Command):
    def __init__(self, status: bool):
        self.message_type = ResponseTradeUserToUserCommand.__name__
        self.status = status

    @classmethod
    def from_dict(cls, obj: dict):
        return ResponseTradeUserToUserCommand(status=obj["status"])


class RequestTradesReceivedUserCommand(Command):
    def __init__(self, user_id: int) -> None:
        self.message_type = RequestTradesReceivedUserCommand.__name__
        self.user_id = user_id


class TradeItem:
    def __init__(
        self,
        trade_id: int,
        username_orig: str,
        username_dest: str,
        stickers_orig: List[Stickers],
        stickers_dest: List[Stickers],
        status: entity.Status,
    ) -> None:
        self.trade_id = trade_id
        self.username_orig = username_orig
        self.username_dest = username_dest
        self.stickers_orig = stickers_orig
        self.stickers_dest = stickers_dest
        self.status = status

    def as_dict(self):
        return {
            "trade_id": self.trade_id,
            "username_orig": self.username_orig,
            "username_dest": self.username_dest,
            "stickers_orig": [s.as_dict() for s in self.stickers_orig],
            "stickers_dest": [s.as_dict() for s in self.stickers_dest],
            "status": self.status.value,
        }

    @staticmethod
    def from_dict(obj: dict):
        return TradeItem(
            obj["trade_id"],
            obj["username_orig"],
            obj["username_dest"],
            [Stickers.from_dict(s) for s in obj["stickers_orig"]],
            [Stickers.from_dict(s) for s in obj["stickers_dest"]],
            Status(obj["status"])
        )


class ResponseTradesReceivedUserCommand(Command):
    def __init__(self, trades: List[TradeItem]) -> None:
        self.message_type = ResponseTradesReceivedUserCommand.__name__
        self.trades = trades

    def as_dict(self):
        return {
            "message_type": self.message_type,
            "trades_received": [t.as_dict() for t in self.trades],
        }

    @staticmethod
    def from_dict(obj: dict):
        return ResponseTradesReceivedUserCommand(
            [TradeItem.from_dict(t) for t in obj["trades_received"]]
        )


class RequestAnswerTradeCommand(Command):
    def __init__(self, trade_id: int, accept: bool):
        self.message_type = RequestAnswerTradeCommand.__name__
        self.accept = accept
        self.trade_id = trade_id


class ResponseAnswerTradeCommand(Command):
    def __init__(self, status: bool):
        self.message_type = ResponseAnswerTradeCommand.__name__
        self.status = status

    @classmethod
    def from_dict(cls, obj: dict):
        return ResponseAnswerTradeCommand(status=obj["status"])


class RequestCreateUserCommand(Command):
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.message_type = RequestCreateUserCommand.__name__


class ResponseCreateUserCommand(Command):
    def __init__(self, status: bool):
        self.message_type = ResponseCreateUserCommand.__name__
        self.status = status

    @classmethod
    def from_dict(cls, obj: dict):
        return ResponseCreateUserCommand(status=obj["status"])


class RequestLoginCommand(Command):
    def __init__(self, username: str, password: str):
        self.message_type = RequestLoginCommand.__name__
        self.username = username
        self.password = password

    @classmethod
    def from_dict(cls, obj: dict):
        return RequestLoginCommand(username=obj["username"], password=obj["password"])


class ResponseLoginCommand(Command):
    def __init__(self, user_id: int):
        self.message_type = ResponseLoginCommand.__name__
        self.user_id = user_id

    @classmethod
    def from_dict(cls, obj: dict):
        return ResponseLoginCommand(obj["user_id"])


class RequestUserCommand(Command):
    def __init__(self, user_id: int):
        self.message_type = RequestUserCommand.__name__
        self.user_id = user_id


class ResponseUserCommand(Command):
    def __init__(self, user: entity.Users):
        self.message_type = ResponseUserCommand.__name__
        self.user = user

    def as_dict(self):
        return {"message_type": self.message_type, "user": self.user.as_dict()}

    @classmethod
    def from_dict(cls, obj: dict):
        return ResponseUserCommand(entity.Users.from_dict(obj["user"]))


class RequestAllUsersCommand(Command):
    def __init__(self) -> None:
        self.message_type = RequestAllUsersCommand.__name__


class ResponseAllUsersCommand(Command):
    def __init__(self, users: List[entity.Users]):
        self.users = users
        self.message_type = ResponseAllUsersCommand.__name__

    def as_dict(self):
        return {
            "users": [u.as_dict(stickers=False) for u in self.users],
            "message_type": self.message_type,
        }

    @classmethod
    def from_dict(cls, obj: dict):
        return ResponseAllUsersCommand(
            users=[entity.Users.from_dict(d) for d in obj["users"]]
        )


class RequestListStickersUserCommand(Command):
    def __init__(self, username) -> None:
        self.message_type = RequestListStickersUserCommand.__name__
        self.username = username


class ResponseListStickersUserCommand(Command):
    def __init__(self, stickers: List[entity.Stickers]):
        self.stickers = stickers
        self.message_type = ResponseListStickersUserCommand.__name__

    @classmethod
    def from_dict(cls, obj: dict):
        return ResponseListStickersUserCommand(
            [entity.Stickers.from_dict(s) for s in obj["stickers"]]
        )

    def as_dict(self):
        return {
            "message_type": ResponseListStickersUserCommand.__name__,
            "stickers": [s.as_dict() for s in self.stickers],
        }
