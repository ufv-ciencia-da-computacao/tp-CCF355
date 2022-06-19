from models.repository.DBConfig import AlbumCredentials, SQLiteConnection
from models.repository import repo
from models.service.StickersPack import StickersPack

if __name__ == "__main__":
    con = SQLiteConnection.get_connection(AlbumCredentials.host)
    session = SQLiteConnection.session[AlbumCredentials.host]

    with session.begin() as sesh:
        stickers_repo = repo.StickersRepository(sesh)
        ls_repo = repo.ListStickersRepository(sesh)
        user_repo = repo.UsersRepository(sesh)
        # sp = StickersPack(stickers_repo, ls_repo)

        # sp.add_pack2user(1)
        user = user_repo.get(1)

        print(ls_repo.get_duplicated_stickers_by_user_id(1))
