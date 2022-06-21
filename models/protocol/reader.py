from email import message
import command


class Reader:
    @staticmethod
    def read(data: dict):
        message_type = data["message_type"]

        if message_type == command.CreateUserCommand.__name__:
            pass
        elif message_type == command.LoginCommand.__name__:
            pass
        elif message_type == command.AcceptTradeCommand.__name__:
            pass
        elif message_type == command.TradeUserToSystemCommand.__name__:
            pass
        elif message_type == command.TradeUserToUserCommand.__name__:
            pass
        elif message_type == command.AcceptTradeCommand.__name__:
            pass
        elif message_type == command.FilterListStickersCommand.__name__:
            pass
        elif message_type == command.ViewListStickersCommand.__name__:
            pass
        elif message_type == command.ViewListUserStickersCommand.__name__:
            pass
