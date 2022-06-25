from asyncio import set_child_watcher
from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
from models.service.StickersPack import StickersPack
from models.protocol import command
import json
from models.domain.entity import Users
from models.domain.entity import Stickers
from middleware.serverSocket import ServerSocket
from sqlalchemy.orm import sessionmaker, scoped_session

if __name__ == "__main__":
    con = SQLiteConnection.get_connection(AlbumCredentials.host)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=con))

    session.begin_nested()
    stickers_repo = repo.StickersRepository(session)
    ls_repo = repo.ListStickersRepository(session)
    user_repo = repo.UsersRepository(session)
    # sp = StickersPack(stickers_repo, ls_repo)

    # sp.add_pack2user(1)
    # user = user_repo.get(1)

    ss = ServerSocket(user_repo, stickers_repo, ls_repo)
    ss.listen()
    # c = command.ViewListUserStickersCommand(user)
    # print(c.execute())
    # stickers = stickers_repo.list()
    # c = command.ViewListStickersCommand(stickers)
    # print(c.execute())

    # trade = TradeUserToUserCommand(10, [1,2,3], 5, [4,5,6])
    # print(type(json.dumps(trade.as_dict())))

# if __name__ == "__main__":
