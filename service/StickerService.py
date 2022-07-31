from models.domain.entity import Stickers
from models.repository.repo import UsersRepository


class StickerService:
    def __init__(self, us_repo: UsersRepository) -> None:
        super().__init__()
        self.us_repo = us_repo

    def list_stickers(self, username):
        user = self.us_repo.get(username=username)
        resp = []
        if user is not None:
            for s in user.stickers:
                s: Stickers
                resp.append(
                    Stickers(
                        playername=s.playername,
                        country=s.country,
                        rarity=s.rarity,
                        id=s.id,
                        photo=s.photo,
                    ).as_dict()
                )
        return resp
