from ..repository.repo import TradeRequestsRepository, UsersRepository
from ..domain.entity import Status, TradeRequest


class TradeStickers:
    def __init__(
        self, tr_repo: TradeRequestsRepository, us_repo: UsersRepository
    ) -> None:
        self.tr_repo = tr_repo
        self.us_repo = us_repo

    def request_trade(
        self, user_sender_id, user_receiver_id, sticker_sender_id, sticker_receiver_id
    ):
        tr_request = TradeRequest(
            user_sender_id=user_sender_id,
            user_receiver_id=user_receiver_id,
            sticker_sender_id=sticker_sender_id,
            sticker_receiver_id=sticker_receiver_id,
        )

        self.tr_repo.add(tr_request)

    def get_all_trades_accepted(self, user_id):
        return self.tr_repo.get_by_status(user_id, Status.accepted)

    def get_all_trades_pendent(self, user_id):
        return self.tr_repo.get_by_status(user_id, Status.pendent)

    def get_all_trades_recused(self, user_id):
        return self.tr_repo.get_by_status(user_id, Status.recused)
