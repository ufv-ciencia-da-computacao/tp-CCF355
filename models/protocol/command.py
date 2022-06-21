from abc import (
    ABC,
    abstractmethod,
)
import json

from .Encoder import CompleteUserEncoder, CreateUserEncoder

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
        return json.dumps(dict(self), cls=CreateUserEncoder, ensure_ascii=False)

    def __iter__(self):
        yield from {"user": self.user, "message_type": self.message_type}.items()

    def __repr__(self):
        return self.__str__()


class LoginCommand(Command):
    def __init__(self, user: entity.Users) -> None:
        self.user = user
        self.message_type = LoginCommand.__name__

    def execute(self) -> str:
        return json.dumps(dict(self), cls=CompleteUserEncoder, ensure_ascii=False)

    def __iter__(self):
        yield from {"user": self.user, "message_type": self.message_type}.items()

    def __repr__(self):
        return self.__str__()


class ViewListUserStickersCommand(Command):
    def execute(self):
        pass


class ViewListStickersCommand(Command):
    def execute(self):
        pass


class FilterListStickersCommand(Command):
    def execute(self):
        pass
