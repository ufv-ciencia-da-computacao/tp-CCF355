import command
import json


class Reader:
    @staticmethod
    def read(data: str):
        data = json.loads(data)
        message_type = data["message_type"]

        if message_type == command.RequestCreateLoginCommand.__name__:
            pass
        elif message_type == command.RequestListUserStickersCommand.__name__:
            pass
        elif message_type == command.AcceptTradeCommand.__name__:
            pass
        elif message_type == command.TradeUserToUserCommand.__name__:
            pass
        elif message_type == command.AcceptTradeCommand.__name__:
            pass
