import abc
import string
from typing import List
from contextlib import contextmanager
import sqlalchemy
from ..domain import entity
from sqlalchemy.sql.expression import func, select
from sqlalchemy.orm import Session
from sqlalchemy import update


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, ent):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref):
        raise NotImplementedError


class StickersRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, sticker: entity.Stickers):
        self.session.add(sticker)
        self.session.commit()

    def get(self, stickers_id: int) -> entity.Stickers:
        stmt = select(entity.Stickers).filter_by(reference=stickers_id)
        return self.session.execute(stmt).one()

    def get_by_rarity(self, rarity: int) -> List[entity.Stickers]:
        stmt = (
            select(entity.Stickers)
            .where(entity.Stickers.rarity == rarity)
            .order_by(func.random())
        )
        return self.session.execute(stmt).first()

    def list(self):
        return self.session.query(entity.Stickers).all()


class UsersRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: entity.Users):
        try:
            self.session.add(user)
        except:
            self.session.rollback()
            raise
        else:
            self.session.commit()

    def get(self, username: string) -> entity.Users:    
        return self.session.query(entity.Users).filter_by(username=username).one()

    def get_by_id(self, id: int) -> entity.Users:
        return self.session.query(entity.Users).filter_by(id=id).one()

    def list(self):
        return self.session.query(entity.Users).all()


class ListStickersRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, list_sticker: entity.ListStickers):
        try:
            self.session.add(list_sticker)
        except:
            self.session.rollback()
            raise
        else:
            self.session.commit()

    def get(self, user_id: int) -> entity.ListStickers:
        return self.session.query(entity.ListStickers).filter_by(user_id=user_id).one()

    def get_by_user_id_and_by_sticker_id(
        self, user_id: int, sticker_id: int
    ) -> entity.ListStickers:
        print("repo.ListStickersRepository.get_by_user_id_and_by_sticker_id", user_id, sticker_id)
        return (
            self.session.query(entity.ListStickers)
            .filter_by(user_id=user_id)
            .filter_by(sticker_id=sticker_id)
            .first()
        )

    def get_duplicated_stickers_by_user_id(self, user_id: int) -> entity.ListStickers:
        return (
            self.session.query(
                entity.ListStickers, func.count(entity.ListStickers.sticker_id)
            )
            .filter_by(user_id=user_id)
            .group_by(entity.ListStickers.sticker_id)
            .having(func.count(entity.ListStickers.sticker_id) > 1)
            .all()
        )

    def update_list_stickers(self, id: int, new_user_id: int) -> None:
        print("repo.ListStickerRepository.update_list_sticker", id, new_user_id)
        try:
            self.session.query(entity.ListStickers).filter(
                entity.ListStickers.id == id
            ).update(
                {entity.ListStickers.user_id: new_user_id}, synchronize_session=False
            )
        except:
            self.session.rollback()
            raise
        else:
            self.session.commit()

    def list(self):
        return self.session.query(entity.ListStickers).all()


class TradeRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, trade: entity.Trade):
        try:
            self.session.add(trade)
        except:
            self.session.rollback()
            raise
        else:
            self.session.commit()

    def get(self, id) -> entity.Trade:
        return self.session.query(entity.Trade).filter_by(id=id).one()

    def get_by_sender_id(self, user_sender_id: int) -> List[entity.Trade]:
        return (
            self.session.query(entity.Trade)
            .filter_by(user_sender_id=user_sender_id)
            .all()
        )

    def get_by_receiver_id(self, user_receiver_id: int) -> List[entity.Trade]:
        return (
            self.session.query(entity.Trade)
            .filter_by(user_receiver_id=user_receiver_id)
            .all()
        )

    def get_by_status(self, user_sender_id: int, status: int) -> entity.Trade:
        return (
            self.session.query(entity.TradeRequest)
            .filter_by(user_sender_id=user_sender_id, status=status)
            .one()
        )

    def update_trade_status(self, id: int, status: int) -> None:
        try:
            self.session.query(entity.Trade).filter(entity.Trade.id == id).update(
                {entity.Trade.status: status}, synchronize_session=False
            )
        except:
            self.session.rollback()
            raise
        else:
            self.session.commit()

    def list(self):
        return self.session.query(entity.Trade).all()


class TradeStickersRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, trade_request: entity.TradeSticker):
        try:
            self.session.add(trade_request)
        except:
            self.session.rollback()
            raise
        else:
            self.session.commit()

    def get(self, id_trade: int) -> entity.TradeSticker:
        return (
            self.session.query(entity.TradeSticker).filter_by(id_trade=id_trade).all()
        )

    def list(self):
        return self.session.query(entity.TradeRequest).all()
