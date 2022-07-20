from middleware.sticker_pb2_grpc import StickerServiceServicer
from models.domain.entity import Stickers
from models.repository.repo import UsersRepository
from middleware.sticker_pb2 import ListStickerResponse


class StickerService(StickerServiceServicer):
    def __init__(self, us_repo: UsersRepository) -> None:
        super().__init__()
        self.us_repo = us_repo

    def list_stickers(self, request, context):
        user = self.us_repo.get(username=request.username)
        resp = ListStickerResponse()
        if user is not None:
            for s in user.stickers:
                s: Stickers
                resp.sticker.extend(
                    [
                        ListStickerResponse.Sticker(
                            playername=s.playername,
                            country=s.country,
                            rarity=s.rarity,
                            id=s.id,
                            photo=s.photo,
                        )
                    ]
                )
        return resp
