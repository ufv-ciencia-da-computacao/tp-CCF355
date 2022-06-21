from abc import (
    ABC,
    abstractmethod,
)
from codecs import EncodedFile
import json

from models.protocol.Encoder import Encoder

from ..domain import entity


class Command(ABC):

    message_type: str

    @abstractmethod
    def execute(self):
        pass


class TradeUserToUserCommand(Command):  # serialize object
    def execute(self):
        pass


class TradeUserToSystemCommand(Command):
    def execute(self):
        pass


class AcceptTradeCommand(Command):
    def execute(self):
        pass


class CreateUserCommand(Command):
    def __init__(self, user: entity.Users) -> None:
        self.user = user
        self.message_type = CreateUserCommand.__name__

    def execute(self) -> str:
        return json.dumps(dict(self), cls=Encoder, ensure_ascii=False)

    def __iter__(self):
        yield from {"user": self.user, "message_type": self.message_type}.items()

    def __str__(self):
        return json.dumps(dict(self), cls=Encoder, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class LoginCommand(Command):
    def __init__(self, user: entity.Users) -> None:
        self.user = user
        self.message_type = LoginCommand.__name__

    def execute(self) -> str:
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)


class ViewListUserStickersCommand(Command):
    def execute(self):
        pass


class ViewListStickersCommand(Command):
    def execute(self):
        pass


class FilterListStickers(Command):
    def execute(self):
        pass
