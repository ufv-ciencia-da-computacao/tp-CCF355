from models.domain import entity
from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
import json

if __name__ == "__main__":
    con = SQLiteConnection.get_connection(AlbumCredentials.host)
    session = SQLiteConnection.session[AlbumCredentials.host]

    entity.create_db(con)
    with open('data/players.json') as f:
        players = json.load(f)
    for d in players:
        s = entity.Stickers(country=d['country'], playername=d['playername'], rarity=d['rarity'])
        with session.begin() as sesh: 
            stickers_repo = repo.StickersRepository(sesh)
            stickers_repo.add(s)