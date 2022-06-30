from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
from middleware.serverSocket import ServerSocket
from sqlalchemy.orm import sessionmaker, scoped_session

if __name__ == "__main__":
    con = SQLiteConnection.get_connection(AlbumCredentials.host)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=con))

    ss = ServerSocket(session=session)
    ss.listen()
