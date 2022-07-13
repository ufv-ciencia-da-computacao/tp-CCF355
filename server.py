from concurrent import futures
from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
from sqlalchemy.orm import sessionmaker, scoped_session

import grpc
from service.StickerService import StickerService
from service.UserService import UserService
from service.TradeService import TradeService
import middleware.user_pb2_grpc as user_pb2_grpc
import middleware.sticker_pb2_grpc as sticker_pb2_grpc
import middleware.trade_pb2_grpc as trade_pb2_grpc

if __name__ == "__main__":
    con = SQLiteConnection.get_connection(AlbumCredentials.host)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=con))

    s_repo = repo.StickersRepository(session)
    ls_repo = repo.ListStickersRepository(session)
    us_repo = repo.UsersRepository(session)
    t_repo = repo.TradeRepository(session)
    tr_repo = repo.TradeStickersRepository(session)
    
    server = grpc.server(futures.ThreadPoolExecutor())
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(us_repo, s_repo, ls_repo), server)
    sticker_pb2_grpc.add_StickerServiceServicer_to_server(StickerService(us_repo), server)
    trade_pb2_grpc.add_TradeServiceServicer_to_server(TradeService(us_repo, ls_repo, t_repo, tr_repo), server)
    server.add_insecure_port("localhost:5555")
    server.start()
    server.wait_for_termination()
