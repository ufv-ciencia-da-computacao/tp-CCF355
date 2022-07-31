from models.domain import entity
from models.repository.repo import (
    ListStickersRepository,
    StickersRepository,
    TradeRepository,
    TradeStickersRepository,
    UsersRepository,
)
from service.TradeStickers import TradeStickersService


class TradeService:
    def __init__(
        self,
        us_repo: UsersRepository,
        ls_repo: ListStickersRepository,
        t_repo: TradeRepository,
        ts_repo: TradeStickersRepository,
    ) -> None:
        super().__init__()
        self.us_repo = us_repo
        self.t_repo = t_repo
        self.trade_stickers = TradeStickersService(
            t_repo=t_repo, tr_repo=ts_repo, us_repo=us_repo, ls_repo=ls_repo
        )

    def request_trade(self, my_username, other_username, my_stickers, other_stickers):
        try:
            user_orig = self.us_repo.get(my_username)
            user_dest = self.us_repo.get(other_username)
            trade = self.trade_stickers.request_trade(
                user_orig.id,
                user_dest.id,
                [s for s in my_stickers],
                [s for s in other_stickers],
            )
            status = True
        except Exception:
            status = False

        return status

    def answer_trade(self, trade_id, accept):
        try:
            self.trade_stickers.answer_trade(trade_id, accept)
            status = True
        except Exception:
            status = False

        return status

    def get_trades(self, username):
        user = self.us_repo.get(username)
        trades = self.t_repo.get_by_receiver_id(user.id)

        resp = []

        for t in trades:
            if t.status != entity.Status.pendent:
                continue

            received = []
            sent = []

            for ts in t.trades_stickers:
                if ts.receiver_sender == entity.ReceiverSender.sender:
                    received.append(ts.sender_sticker)
                else:
                    sent.append(ts.sender_sticker)

            resp.append(
                {
                    "to_send": [
                        entity.Stickers(
                            playername=s.playername,
                            country=s.country,
                            rarity=s.rarity,
                            id=s.id,
                        ).as_dict()
                        for s in sent
                    ],
                    "to_receive": [
                        entity.Stickers(
                            playername=s.playername,
                            country=s.country,
                            rarity=s.rarity,
                            id=s.id,
                        ).as_dict()
                        for s in received
                    ],
                    "username": t.sender_user.username,
                    "status": t.status.pendent.name,
                    "trade_id": t.id,
                }
            )

        return resp
