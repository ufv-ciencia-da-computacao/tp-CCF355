from middleware.trade_pb2_grpc import TradeServiceServicer
from middleware.trade_pb2 import TradeResponse
from models.repository.repo import ListStickersRepository, StickersRepository, TradeRepository, TradeStickersRepository, UsersRepository
from service.TradeStickers import TradeStickersService

class TradeService(TradeServiceServicer):
    def __init__(self, 
        us_repo : UsersRepository, 
        ls_repo : ListStickersRepository,
        t_repo : TradeRepository,
        ts_repo : TradeStickersRepository 
    ) -> None:
        super().__init__()
        self.us_repo = us_repo
        self.trade_stickers = TradeStickersService(
            t_repo=t_repo,
            tr_repo=ts_repo,
            us_repo=us_repo,
            ls_repo=ls_repo 
        )

    def request_trade(self, request, context):
        resp = TradeResponse(status=False)

        try:
            user_orig = self.us_repo.get(request.my_username)
            user_dest = self.us_repo.get(request.other_username)
            trade = self.trade_stickers.request_trade(
                user_orig.id,
                user_dest.id,
                [s.id for s in request.my_stickers],
                [s.id for s in request.other_stickers]
            )
            print(trade)
            resp.status = True
        except Exception:
            pass
            
        return resp

    def answer_trade(self, request, context):
        return super().answer_trade(request, context)

    def get_trades(self, request, context):
        return super().get_trades(request, context)