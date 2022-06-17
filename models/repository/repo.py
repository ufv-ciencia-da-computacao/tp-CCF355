import abc
from ..domain import entity

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, ent):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref):
        raise NotImplementedError


class StickersRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, sticker: entity.Stickers):
        self.session.add(sticker)

    def get(self, stickers_id: int) -> entity.Stickers:
        return self.session.query(entity.Stickers).filter_by(reference=stickers_id).one()

    def list(self):
        return self.session.query(entity.Stickers).all()


class UsersRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, user: entity.Users):
        self.session.add(user)

    def get(self, user_id: int) -> entity.Users:
        return self.session.query(entity.Users).filter_by(user_id=user_id).one()

    def list(self):
        return self.session.query(entity.Users).all()


class ListStickersRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, list_sticker: entity.ListStickers):
        self.session.add(list_sticker)

    def get(self, user_id: int) -> entity.ListStickers:
        return self.session.query(entity.ListStickers).filter_by(user_id=user_id).one()

    def list(self):
        return self.session.query(entity.ListStickers).all()