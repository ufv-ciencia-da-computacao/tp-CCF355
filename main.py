from models.domain import entity
from models.repository.DBConfig import AlbumCredentials, SQLiteConnection


if __name__ == "__main__":
    con = SQLiteConnection.get_connection(AlbumCredentials.host)
    entity.create_db(con)