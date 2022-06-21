from selectors import SelectSelector
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
import enum
from sqlalchemy.orm import declarative_base, relationship

from ..repository.DBConfig import SQLiteConnection, AlbumCredentials
import json
from models.protocol.Encoder import CompleteUserEncoder

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    stickers = relationship(
        "Stickers", secondary="list_stickers", back_populates="users"
    )
    trades_sent = relationship(
        "TradeRequest", primaryjoin="TradeRequest.user_sender_id == Users.id"
    )
    trades_received = relationship(
        "TradeRequest", primaryjoin="TradeRequest.user_receiver_id == Users.id"
    )

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __iter__(self):
        yield from {
            "id": self.id,
            "username": self.username,
            "stickers": self.stickers,
            "trades_sent": self.trades_sent,
            "trades_received": self.trades_received,
        }.items()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(dict(self), cls=CompleteUserEncoder, ensure_ascii=False)

    def complete_to_json(self):
        to_return = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }
        stickers = []
        for stk in self.stickers.__iter__():
            s = stk.__dict__
            s.pop("_sa_instance_state", None)
            stickers.append(s)

        to_return["stickers"] = stickers

        trades_sent = []
        for tdse in self.trades_sent.__iter__():
            t = tdse.__dict__
            t.pop("_sa_instance_state", None)
            trades_sent.append(t)

        to_return["trades_sent"] = trades_sent

        trades_received = []
        for tdre in self.trades_received.__iter__():
            t = tdre.__dict__
            t.pop("_sa_instance_state", None)
            trades_received.append(t)

        to_return["trades_received"] = trades_received

        return to_return

    def create_to_json(self):
        to_return = {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }

        return to_return


class Stickers(Base):
    __tablename__ = "stickers"

    id = Column(Integer, primary_key=True)
    playername = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    rarity = Column(Integer, nullable=False)
    # photo
    users = relationship("Users", secondary="list_stickers", back_populates="stickers")

    def __init__(self, playername: str, country: str, rarity: int):
        self.playername = playername
        self.country = country
        self.rarity = rarity

    def __iter__(self):
        yield from {
            "id": self.id,
            "playername": self.playername,
            "country": self.country,
            "rarity": self.rarity,
        }.items()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(dict(self), cls=Encoder, ensure_ascii=False)

    def to_json(self):
        return self.__str__()

    # def __repr__(self) -> str:
    #     return f"(id:{self.id}, playername: {self.playername}, country: {self.country}, rarity: {self.rarity})"


class ListStickers(Base):
    __tablename__ = "list_stickers"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    sticker_id = Column(ForeignKey("stickers.id"))

    def __init__(self, user_id: int, sticker_id: int):
        self.user_id = user_id
        self.sticker_id = sticker_id

    def __iter__(self):
        yield from {
            "id": self.id,
            "user_id": self.user_id,
            "sticker_id": self.sticker_id,
        }.items()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(dict(self), cls=Encoder, ensure_ascii=False)

    def to_json(self):
        return self.__str__()


class Status(enum.Enum):
    pendent = 1
    recused = 2
    accepted = 3

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(dict(self), cls=Encoder, ensure_ascii=False)

    def to_json(self):
        return self.__str__()


class TradeRequest(Base):
    __tablename__ = "trade_request"

    id = Column(Integer, primary_key=True)
    user_sender_id = Column(Integer, ForeignKey("users.id"))
    user_receiver_id = Column(Integer, ForeignKey("users.id"))
    sticker_sender_id = Column(Integer, ForeignKey("stickers.id"))
    sticker_receiver_id = Column(Integer, ForeignKey("stickers.id"))
    status = Column(Enum(Status), nullable=False)

    receiver_sticker = relationship("Stickers", foreign_keys=[sticker_receiver_id])
    sender_sticker = relationship("Stickers", foreign_keys=[sticker_sender_id])
    receiver_user = relationship(
        "Users", foreign_keys=[user_receiver_id], back_populates="trades_received"
    )
    sender_user = relationship(
        "Users", foreign_keys=[user_sender_id], back_populates="trades_sent"
    )

    def __init__(
        self,
        user_sender_id,
        user_receiver_id,
        sticker_sender_id,
        sticker_receiver_id,
        status=Status.pendent,
    ) -> None:
        self.user_sender_id = user_sender_id
        self.user_receiver_id = user_receiver_id
        self.sticker_sender_id = sticker_sender_id
        self.sticker_receiver_id = sticker_receiver_id
        self.status = status

    def __iter__(self):
        yield from {
            "id": self.id,
            "receiver_sticker": self.receiver_sticker,
            "sender_sticker": self.sender_sticker,
            "receiver_user": self.receiver_user,
            "sender_user": self.sender_user,
            "status": self.status,
        }.items()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps(dict(self), cls=Encoder, ensure_ascii=False)

    def to_json(self):
        return self.__str__()


def create_db(con):
    Base.metadata.create_all(con)
