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
    def __init__(self, user_orig: int, stickers_user_orig: list, user_dest: int, stickers_user_dest: list):
        self.message_type = TradeUserToUserCommand.__name__
        self.user_orig = user_orig
        self.user_dest = user_dest
        self.stickers_user_orig = stickers_user_orig
        self.stickers_user_dest = stickers_user_dest

    def execute(self):
        pass
    
    def as_dict(self):
        return self.__dict__


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
