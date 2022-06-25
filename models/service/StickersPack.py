from typing import List
import random
from ..repository.repo import StickersRepository, ListStickersRepository
from ..domain.entity import ListStickers, Stickers
from models.domain import entity


class StickersPack:
    def __init__(
        self, stickersRepo: StickersRepository, ls_repo: ListStickersRepository
    ) -> None:
        self.stickers_repo = stickersRepo
        self.ls_repo = ls_repo
        self.probability = [82, 15, 3]
        self.rarity = [1, 2, 3]
        self.rarities = random.choices(self.rarity, weights=(self.probability), k=4)

    def _get_pack(self) -> List[Stickers]:
        pack = []
        for r in self.rarities:
            s = self.stickers_repo.get_by_rarity(r)
            pack.append(*s)

        return pack

    def add_pack2user(self, user: entity.Users):
        print(user.as_dict())
        pack = self._get_pack()

        for s in pack:
            self.ls_repo.add(ListStickers(user.id, s.id))

    def trade_duplicated_cards(self, user_id: int):
        pass

    def __repr__(self) -> str:
        return "\n".join(map(Stickers.__repr__, self.pack))
