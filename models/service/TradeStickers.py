from ..repository.repo import (
    ListStickersRepository,
    UsersRepository,
    TradeStickersRepository,
    TradeRepository,
)
from ..domain.entity import ReceiverSender, Status, Trade, TradeSticker
from typing import List
import itertools


class TradeStickersService:
    def __init__(
        self,
        t_repo: TradeRepository,
        tr_repo: TradeStickersRepository,
        us_repo: UsersRepository,
        ls_repo: ListStickersRepository,
    ) -> None:
        self.t_repo = t_repo
        self.tr_repo = tr_repo
        self.us_repo = us_repo
        self.ls_repo = ls_repo

    def request_trade(
        self,
        user_sender_id,
        user_receiver_id,
        sticker_sender_id: List[int],
        sticker_receiver_id: List[int],
    ) -> Trade:
        try:
            obj = Trade(
                user_sender_id=user_sender_id, user_receiver_id=user_receiver_id
            )
            self.t_repo.add(obj)

            for s in sticker_sender_id:
                tr_request = TradeSticker(
                    id_trade=obj.id, sticker_id=s, receiver_sender=ReceiverSender.sender
                )

                self.tr_repo.add(tr_request)

            for s in sticker_receiver_id:
                tr_request = TradeSticker(
                    id_trade=obj.id,
                    sticker_id=s,
                    receiver_sender=ReceiverSender.receiver,
                )

                self.tr_repo.add(tr_request)
            return obj
        except:
            raise

    def answer_trade(self, trade_id, answer):
        trade = self.t_repo.get(trade_id).as_dict()
        print(trade)
        user_sender_id = trade["user_sender_id"]
        user_receiver_id = trade["user_receiver_id"]

        error = False
        if answer == Status.recused:
            self.t_repo.update_trade_status(trade.id, Status.recused)
        else:
            error = False
            for ss in trade["stickers_sent"]:
                sticker_from_ls = self.ls_repo.get_by_user_id_and_by_sticker_id(
                    user_sender_id, ss["sticker"]["id"]
                )
                if sticker_from_ls is None:
                    error = True

            for sr in trade["stickers_received"]:
                sticker_from_ls = self.ls_repo.get_by_user_id_and_by_sticker_id(
                    user_receiver_id, sr["sticker"]["id"]
                )
                if sticker_from_ls is None:
                    print(user_receiver_id, sr["id"])
                    error = True

            if error == False:
                self.t_repo.update_trade_status(trade["id"], Status.accepted)
                for ss in trade["stickers_sent"]:
                    ls = self.ls_repo.get_by_user_id_and_by_sticker_id(
                        user_sender_id, ss["sticker"]["id"]
                    )

                    self.ls_repo.update_list_stickers(ls.id, user_receiver_id)

                for sr in trade["stickers_received"]:
                    ls = self.ls_repo.get_by_user_id_and_by_sticker_id(
                        user_receiver_id, sr["sticker"]["id"]
                    )
                    self.ls_repo.update_list_stickers(ls.id, user_sender_id)
            else:
                raise

    def get_all_trades_accepted(self, user_id):
        return self.t_repo.get_by_status(user_id, Status.accepted)

    def get_all_trades_pendent(self, user_id):
        return self.t_repo.get_by_status(user_id, Status.pendent)

    def get_all_trades_recused(self, user_id):
        return self.t_repo.get_by_status(user_id, Status.recused)
