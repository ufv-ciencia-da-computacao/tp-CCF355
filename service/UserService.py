from models.domain import entity

from models.repository.repo import (
    ListStickersRepository,
    StickersRepository,
    UsersRepository,
)
from service.StickersPack import StickersPack


class UserService:
    def __init__(
        self,
        us_repo: UsersRepository,
        s_repo: StickersRepository,
        ls_repo: ListStickersRepository,
    ) -> None:
        super().__init__()
        self.us_repo = us_repo
        self.stickers_pack = StickersPack(s_repo, ls_repo)

    def login(self, username, password):
        user = self.us_repo.get(username)
        if user is not None and user.password == password:
            return user.id
        return -1

    def register(self, username, password):
        user = entity.Users(username=username, password=password)
        try:
            self.us_repo.add(user=user)
            self.stickers_pack.add_pack2user(user=self.us_repo.get(user.username))
            status = True
        except Exception:
            status = False

        return status
