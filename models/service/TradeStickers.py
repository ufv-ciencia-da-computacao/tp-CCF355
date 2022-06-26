from ..repository.repo import UsersRepository, TradeRequestRepository, TradeRepository
from ..domain.entity import Status, Trade, TradeRequest
from typing import List
import itertools


class TradeStickers:
    def __init__(
        self,
        t_repo: TradeRepository,
        tr_repo: TradeRequestRepository,
        us_repo: UsersRepository,
    ) -> None:
        self.t_repo = t_repo
        self.tr_repo = tr_repo
        self.us_repo = us_repo

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

            stickers = itertools.zip_longest(sticker_sender_id, sticker_receiver_id)

            for s in stickers:
                sticker_sender, sticker_receiver = s
                tr_request = TradeRequest(
                    id_trade=obj.id,
                    sticker_sender_id=sticker_sender,
                    sticker_receiver_id=sticker_receiver,
                )

                self.tr_repo.add(tr_request)
            return obj
        except:
            raise

    def get_all_trades_accepted(self, user_id):
        return self.t_repo.get_by_status(user_id, Status.accepted)

    def get_all_trades_pendent(self, user_id):
        return self.t_repo.get_by_status(user_id, Status.pendent)

    def get_all_trades_recused(self, user_id):
        return self.t_repo.get_by_status(user_id, Status.recused)
