from models.domain import entity
from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
from models.protocol import command
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

    for d in players:
        s = entity.Stickers(
            country=d["country"], playername=d["playername"], rarity=d["rarity"]
        )
        stickers_repo.add(s)
