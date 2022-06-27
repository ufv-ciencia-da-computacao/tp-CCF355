from models.domain import entity
from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
from models.protocol import command
from models.service.StickersPack import StickersPack
import json
from sqlalchemy.orm import sessionmaker, scoped_session

if __name__ == "__main__":
    con = SQLiteConnection.get_connection(AlbumCredentials.host)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=con))

    session.begin_nested()
    entity.create_db(con)

    with open("data/players.json") as f:
        players = json.load(f)

    stickers_repo = repo.StickersRepository(session)
    users_repo = repo.UsersRepository(session)
    ls_repo = repo.ListStickersRepository(session)

    stickerspack = StickersPack(stickers_repo, ls_repo)

    for d in players:
        s = entity.Stickers(
            country=d["country"], playername=d["playername"], rarity=d["rarity"]
        )
        stickers_repo.add(s)

    with open("data/users.json") as f:
        users = json.load(f)

    for d in users:
        u = entity.Users(username=d["username"], password=d["password"])
        users_repo.add(u)
        stickerspack.add_pack2user(user=users_repo.get(u.username))
