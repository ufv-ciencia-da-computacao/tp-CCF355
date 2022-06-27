from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
from middleware.serverSocket import ServerSocket
from sqlalchemy.orm import sessionmaker, scoped_session

if __name__ == "__main__":
    con = SQLiteConnection.get_connection(AlbumCredentials.host)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=con))

    session.begin_nested()
    stickers_repo = repo.StickersRepository(session)
    ls_repo = repo.ListStickersRepository(session)
    user_repo = repo.UsersRepository(session)
    t_repo = repo.TradeRepository(session)
    tr_repo = repo.TradeStickersRepository(session)

    ss = ServerSocket(user_repo, stickers_repo, ls_repo, t_repo, tr_repo)
    ss.listen()
