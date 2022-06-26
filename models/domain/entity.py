from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
import enum
from sqlalchemy.orm import declarative_base, relationship

from ..repository.DBConfig import SQLiteConnection, AlbumCredentials
import json

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    stickers = relationship(
        "Stickers", secondary="list_stickers", back_populates="users"
    )
    trades_sent = relationship("Trade", primaryjoin="Trade.user_sender_id == Users.id")
    trades_received = relationship(
        "Trade", primaryjoin="Trade.user_receiver_id == Users.id"
    )

    def __init__(
        self, username: str, password: str, id: int = None, stickers: list = []
    ):
        self.id = id
        self.username = username
        self.password = password
        self.stickers = stickers

    def as_dict(self, stickers=True, password=False, trades=True):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if stickers:
            ret["stickers"] = [stickers.as_dict() for stickers in self.stickers]
        else:
            ret["stickers"] = ""

        if not password:
            ret["password"] = ""

        if trades:
            ret["trades_sent"] = [ts.asdict() for ts in self.trades_sent]
            ret["trades_received"] = [tr.asdict() for tr in self.trades_received]
        else:
            ret["trades_sent"] = ""
            ret["trades_received"] = ""

        return ret

    @classmethod
    def from_dict(cls, obj: dict):
        return Users(
            username=obj["username"],
            password=obj["password"],
            id=obj["id"],
            stickers=[Stickers.from_dict(s) for s in obj["stickers"]],
            trades_sent=[],
            trades_received=[],
        )


class Stickers(Base):
    __tablename__ = "stickers"

    id = Column(Integer, primary_key=True)
    playername = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    rarity = Column(Integer, nullable=False)
    # photo
    users = relationship("Users", secondary="list_stickers", back_populates="stickers")

    def __init__(self, playername: str, country: str, rarity: int, id: int = None):
        self.id = id
        self.playername = playername
        self.country = country
        self.rarity = rarity

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, obj: dict):
        return Stickers(
            playername=obj["playername"],
            country=obj["country"],
            rarity=obj["rarity"],
            id=obj["id"],
        )


class ListStickers(Base):
    __tablename__ = "list_stickers"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    sticker_id = Column(ForeignKey("stickers.id"))

    def __init__(self, user_id: int, sticker_id: int):
        self.user_id = user_id
        self.sticker_id = sticker_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Status(enum.Enum):
    pendent = 1
    recused = 2
    accepted = 3


class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True)
    user_sender_id = Column(Integer, ForeignKey("users.id"))
    user_receiver_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(Status), nullable=False)

    receiver_user = relationship(
        "Users", foreign_keys=[user_receiver_id], back_populates="trades_received"
    )
    sender_user = relationship(
        "Users", foreign_keys=[user_sender_id], back_populates="trades_sent"
    )
    trades_requests = relationship(
        "TradeRequest", primaryjoin="TradeRequest.id_trade == Trade.id"
    )

    def __init__(
        self,
        user_sender_id,
        user_receiver_id,
        status=Status.pendent,
    ) -> None:
        self.user_sender_id = user_sender_id
        self.user_receiver_id = user_receiver_id
        self.status = status

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ret["stickers_traded"] = [tr.as_dict() for tr in self.trades_requests]
        ret["receiver_user"] = self.receiver_user.as_dict()
        ret["sender_id"] = self.sender_user.as_dict()
        return ret


class TradeRequest(Base):
    __tablename__ = "trade_request"

    id = Column(Integer, primary_key=True)
    id_trade = Column(ForeignKey("trade.id"))
    sticker_sender_id = Column(Integer, ForeignKey("stickers.id"), nullable=True)
    sticker_receiver_id = Column(Integer, ForeignKey("stickers.id"), nullable=True)

    receiver_sticker = relationship("Stickers", foreign_keys=[sticker_receiver_id])
    sender_sticker = relationship("Stickers", foreign_keys=[sticker_sender_id])

    def __init__(
        self,
        id_trade,
        sticker_sender_id,
        sticker_receiver_id,
        status=Status.pendent,
    ) -> None:
        self.id_trade = id_trade
        self.sticker_sender_id = sticker_sender_id
        self.sticker_receiver_id = sticker_receiver_id
        self.status = status

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create_db(con):
    Base.metadata.create_all(con)
