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

    def __init__(
        self,
        username: str,
        password: str,
        id: int = None,
        stickers: list = [],
    ):
        self.id = id
        self.username = username
        self.password = password
        self.stickers = stickers

    def as_dict(self, stickers=True, password=False):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if stickers:
            ret["stickers"] = [stickers.as_dict() for stickers in self.stickers]
        else:
            ret["stickers"] = []

        if not password:
            ret["password"] = ""

        return ret

    @classmethod
    def from_dict(cls, obj: dict):
        return Users(
            username=obj["username"],
            password=obj["password"],
            id=obj["id"],
            stickers=[Stickers.from_dict(s) for s in obj["stickers"]],
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


class ReceiverSender(enum.Enum):
    receiver = 1
    sender = 2


class Trade(Base):
    __tablename__ = "trade"

    id = Column(Integer, primary_key=True)
    user_sender_id = Column(ForeignKey("users.id"), nullable=False)
    user_receiver_id = Column(ForeignKey("users.id"), nullable=False)
    status = Column(Enum(Status), nullable=False)

    trades_requests = relationship(
        "TradeSticker", primaryjoin="TradeSticker.id_trade == Trade.id"
    )

    sender_user = relationship("Users", primaryjoin="Users.id == Trade.user_sender_id")

    receiver_user = relationship(
        "Users", primaryjoin="Users.id == Trade.user_receiver_id"
    )

    def __init__(
        self,
        user_sender_id,
        user_receiver_id,
        status=Status.pendent,
        trades_requests=[],
    ) -> None:
        self.user_sender_id = user_sender_id
        self.user_receiver_id = user_receiver_id
        self.status = status
        self.trades_requests = trades_requests

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        stickers_received = []
        stickers_sent = []

        for tr in self.trades_requests:
            if tr.receiver_sender == ReceiverSender.receiver:
                stickers_received.append(tr.as_dict())
            else:
                stickers_sent.append(tr.as_dict())

        ret["stickers_sent"] = stickers_sent
        ret["stickers_received"] = stickers_received
        ret["receiver_user"] = self.receiver_user.as_dict(stickers=False)
        ret["sender_user"] = self.sender_user.as_dict(stickers=False)
        ret["status"] = self.status
        return ret

    def from_dict(self, obj: dict):
        return Trade(
            id=obj["trade"],
            trades_requests=[
                TradeSticker.from_dict(tr) for tr in obj["stickers_traded"]
            ],
            receiver_user=Users.from_dict(obj["receiver_user"]),
            sender_user=Users.from_dict(obj["sender_user"]),
            status=obj["status"],
        )

    def __repr__(self) -> str:
        return f"receiver_user_id = {self.user_receiver_id}, sender_user_id = {self.user_sender_id}"


class TradeSticker(Base):
    __tablename__ = "trade_stickers"

    id = Column(Integer, primary_key=True)
    id_trade = Column(ForeignKey("trade.id"))
    sticker_id = Column(ForeignKey("stickers.id"), nullable=False)
    receiver_sender = Column(Enum(ReceiverSender), nullable=False)

    sender_sticker = relationship(
        "Stickers", primaryjoin="Stickers.id==TradeSticker.sticker_id"
    )

    def __init__(
        self,
        id_trade,
        sticker_id,
        receiver_sender,
    ) -> None:
        self.id_trade = id_trade
        self.sticker_id = sticker_id
        self.receiver_sender = receiver_sender

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ret["sticker"] = self.sender_sticker.as_dict()
        ret["category"] = self.receiver_sender
        return ret

    def from_dict(self, obj: dict):
        print(obj)
        return TradeSticker(
            id=obj["id"],
            id_trade=obj["id_trade"],
            stickers=Stickers.from_dict(obj["stickers"]),
            receiver_sender=obj["receiver_sender"],
        )

    def __repr__(self) -> str:
        return f"id_trade = {self.id_trade}, sticker_id = {self.sticker_id}"


def create_db(con):
    Base.metadata.create_all(con)
