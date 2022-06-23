from models.domain import entity
from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
from models.protocol import command
import json

if __name__ == "__main__":
    con = SQLiteConnection.get_connection(AlbumCredentials.host)
    session = SQLiteConnection.session[AlbumCredentials.host]
    # entity.create_db(con)
    # with open('data/players.json') as f:
    #     players = json.load(f)
    # with session.begin() as sesh:
    #     stickers_repo = repo.StickersRepository(sesh)
    #     users_repo = repo.UsersRepository(sesh)

    #     user = entity.Users("gegen07", "germano")
    #     users_repo.add(user)

    #     for d in players:
    #         s = entity.Stickers(country=d['country'], playername=d['playername'], rarity=d['rarity'])
    #         stickers_repo.add(s)
