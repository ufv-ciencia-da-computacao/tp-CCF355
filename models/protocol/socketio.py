from ..protocol.command import (
    Command,
    RequestAnswerTradeCommand,
    RequestListStickersUserCommand,
    RequestLoginCommand,
    RequestCreateUserCommand,
    RequestTradeUserToUserCommand,
    RequestTradesReceivedUserCommand,
    RequestUserCommand,
    ResponseAllUsersCommand,
    ResponseAnswerTradeCommand,
    ResponseCreateUserCommand,
    ResponseListStickersUserCommand,
    ResponseLoginCommand,
    ResponseTradeUserToUserCommand,
    ResponseTradesReceivedUserCommand,
    ResponseUserCommand,
    TradeItem,
)
import socket
import json
import traceback
import sys

from models.domain import entity
from ..repository import repo
from ..service.StickersPack import StickersPack
from ..service.TradeStickers import TradeStickersService

EOF = 0x05

class ClientDisconnectedException(Exception):
    pass

class Reader:
    def _read_message(sock: socket.socket):
        chunks = []
        while True:
            data = sock.recv(4096)
            if not data:
                raise ClientDisconnectedException()
            if data[len(data) - 1] == EOF:
                chunks.append(str(data[: len(data) - 1].decode("utf-8")))
                break
            else:
                chunks.append(str(data.decode("utf-8")))

        print("socket received:", "".join(chunks))
        return "".join(chunks)


class ReaderRequest(Reader):
    def __init__(
        self,
        us_repo: repo.UsersRepository,
        s_repo: repo.StickersRepository,
        ls_repo: repo.ListStickersRepository,
        t_repo: repo.TradeRepository,
        tr_repo: repo.TradeStickersRepository,
    ) -> None:
        self.us_repo = us_repo
        self.s_repo = s_repo
        self.ls_repo = ls_repo
        self.t_repo = t_repo
        self.tr_repo = tr_repo
        self.stickerspack = StickersPack(s_repo, ls_repo)
        self.tradestickers = TradeStickersService(t_repo, tr_repo, us_repo, ls_repo)

    def read(self, sock: socket.socket):
        data = Reader._read_message(sock)
        data = json.loads(data)
        message_type = data["message_type"]

        cmd = None
        if message_type == RequestCreateUserCommand.__name__:
            u = entity.Users(username=data["username"], password=data["password"])
            try:
                self.us_repo.add(u)
                cmd = ResponseCreateUserCommand(True)
                self.stickerspack.add_pack2user(
                    user=self.us_repo.get(u.username)
                )  # sorteando 100 cartas
            except Exception:
                traceback.print_exception(*sys.exc_info())
                cmd = ResponseCreateUserCommand(False)

        elif message_type == RequestLoginCommand.__name__:
            cmd = ResponseLoginCommand(None)
            try:
                user = self.us_repo.get(data["username"])
                if user is not None and user.password == data["password"]:
                    cmd = ResponseLoginCommand(user_id=user.id)
            except:
                traceback.print_exception(*sys.exc_info())
                # cmd = ErrorCommand()
        elif message_type == RequestListStickersUserCommand.__name__:
            cmd = ResponseListStickersUserCommand(stickers=[])
            try:
                user = self.us_repo.get(data["username"])

                if user is not None:
                    cmd = ResponseListStickersUserCommand(stickers=user.stickers)
            except:
                traceback.print_exception(*sys.exc_info())

        elif message_type == RequestTradeUserToUserCommand.__name__:
            cmd = ResponseTradeUserToUserCommand(False)

            try:
                user_orig = self.us_repo.get(data["user_orig"])
                user_dest = self.us_repo.get(data["user_dest"])

                trade = self.tradestickers.request_trade(
                    user_orig.id,
                    user_dest.id,
                    data["stickers_user_orig"],
                    data["stickers_user_dest"],
                )
                # trade = self.t_repo.get(trade.id)
                cmd = ResponseTradeUserToUserCommand(True)
            except:
                traceback.print_exception(*sys.exc_info())
        elif message_type == RequestTradesReceivedUserCommand.__name__:
            cmd = ResponseTradesReceivedUserCommand([])
            try:
                trades = self.t_repo.get_by_receiver_id(data["user_id"])
                trade_item_list = []
                for t in trades:
                    stickers_received = []
                    stickers_sent = []

                    for ts in t.trades_stickers:
                        if ts.receiver_sender == entity.ReceiverSender.sender:
                            stickers_received.append(ts.sender_sticker)
                        else:
                            stickers_sent.append(ts.sender_sticker)

                    trade_item_list.append(
                        TradeItem(
                            t.id,
                            t.sender_user.username,
                            t.receiver_user.username,
                            stickers_received,
                            stickers_sent,
                            t.status,
                        )
                    )

                cmd = ResponseTradesReceivedUserCommand(trade_item_list)
            except:
                traceback.print_exception(*sys.exc_info())

        elif message_type == RequestAnswerTradeCommand.__name__:
            cmd = ResponseAnswerTradeCommand(False)
            try:
                self.tradestickers.answer_trade(data["trade_id"], data["accept"])
                cmd = ResponseAnswerTradeCommand(True)
            except:
                traceback.print_exception(*sys.exc_info())

        elif message_type == RequestUserCommand.__name__:
            user = self.us_repo.get_by_id(data["user_id"])
            cmd = ResponseUserCommand(user=user)

        return cmd


class ReaderResponse(Reader):
    @staticmethod
    def read(sock: socket.socket):
        data = Reader._read_message(sock)
        data = json.loads(data)
        cmd = None
        if data["message_type"] == ResponseCreateUserCommand.__name__:
            cmd = ResponseCreateUserCommand.from_dict(data)
        elif data["message_type"] == ResponseLoginCommand.__name__:
            cmd = ResponseLoginCommand.from_dict(data)
        elif data["message_type"] == ResponseAllUsersCommand.__name__:
            cmd = ResponseAllUsersCommand.from_dict(data)
        elif data["message_type"] == ResponseListStickersUserCommand.__name__:
            cmd = ResponseListStickersUserCommand.from_dict(data)
        elif data["message_type"] == ResponseUserCommand.__name__:
            cmd = ResponseUserCommand.from_dict(data)
        elif data["message_type"] == ResponseTradeUserToUserCommand.__name__:
            cmd = ResponseTradeUserToUserCommand.from_dict(data)
        elif data["message_type"] == ResponseTradesReceivedUserCommand.__name__:
            cmd = ResponseTradesReceivedUserCommand.from_dict(data)
        elif data["message_type"] == ResponseAnswerTradeCommand.__name__:
            cmd = ResponseAnswerTradeCommand.from_dict(data)
        return cmd


class Writer:
    def _write_string(sock: socket.socket, msg: str) -> None:
        sock.sendall(msg.encode("utf-8"))
        sock.sendall(bytearray([EOF]))

    @staticmethod
    def write_command(sock: socket.socket, cmd: Command) -> str:
        return Writer._write_string(sock, cmd.execute())
