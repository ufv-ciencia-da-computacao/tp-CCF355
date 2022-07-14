from middleware.trade_pb2_grpc import TradeServiceServicer
from middleware.trade_pb2 import AnswerTradeResponse, GetTradesResponse, TradeResponse
from models.domain import entity
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
        self.t_repo = t_repo
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
                [s for s in request.my_stickers],
                [s for s in request.other_stickers]
            )
            resp.status = True
        except Exception:
            pass
            
        return resp

    def answer_trade(self, request, context):
        resp = AnswerTradeResponse(status=False)
        try:
            self.trade_stickers.answer_trade(request.trade_id, request.accept)
            resp.status=True
        except Exception:
            pass

        return resp

    def get_trades(self, request, context):
        user = self.us_repo.get(request.username)
        trades = self.t_repo.get_by_receiver_id(user.id)
        
        resp = GetTradesResponse()

        for t in trades:
            if t.status != entity.Status.pendent:
                continue;

            received = []
            sent = []
            
            for ts in t.trades_stickers:
                if ts.receiver_sender == entity.ReceiverSender.sender:
                    received.append(ts.sender_sticker)
                else:
                    sent.append(ts.sender_sticker)

            resp.trades.extend([
                GetTradesResponse.Trade(
                    to_send=[GetTradesResponse.Trade.Sticker(
                        playername=s.playername,
                        country=s.country,
                        rarity=s.rarity,
                        id=s.id
                    ) for s in sent],

                    to_receive=[GetTradesResponse.Trade.Sticker(
                        playername=s.playername,
                        country=s.country,
                        rarity=s.rarity,
                        id=s.id
                    ) for s in received],
                    
                    username=t.sender_user.username,
                    
                    status=GetTradesResponse.Trade.Status.PENDENT,

                    trade_id=t.id
                )
            ])

        return resp
