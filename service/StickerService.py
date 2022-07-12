from tkinter.tix import S_REGION
import middleware.sticker_pb2
import middleware.sticker_pb2_grpc

from middleware.sticker_pb2_grpc import StickerServiceServicer
from middleware.sticker_pb2 import Sticker
from models.domain.entity import Stickers
from models.repository.repo import UsersRepository

class StickerService(StickerServiceServicer):
    def __init__(self, us_repo: UsersRepository) -> None:
        super().__init__()
        self.us_repo = us_repo

    def list_of_user(self, request, context):
        user = self.us_repo.get(username=request.username)
        if user is not None:
            for s in user.stickers:
                s : Stickers
                yield Sticker(playername=s.playername, country=s.country, rarity=s.rarity)
