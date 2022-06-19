from selectors import SelectSelector
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum
import enum
from sqlalchemy.orm import declarative_base, relationship
from ..repository.DBConfig import SQLiteConnection, AlbumCredentials

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    stickers = relationship(
        "Stickers", secondary="list_stickers", back_populates="users"
    )
    trades_sended = relationship(
        "TradeRequest", primaryjoin="TradeRequest.user_sender_id == Users.id"
    )
    trades_received = relationship(
        "TradeRequest", primaryjoin="TradeRequest.user_receiver_id == Users.id"
    )

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


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

    def __repr__(self) -> str:
        return f"(id:{self.id}, playername: {self.playername}, country: {self.country}, rarity: {self.rarity})"


class ListStickers(Base):
    __tablename__ = "list_stickers"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    sticker_id = Column(ForeignKey("stickers.id"))

    def __init__(self, user_id: int, sticker_id: int):
        self.user_id = user_id
        self.sticker_id = sticker_id


class Status(enum.Enum):
    pendent = 1
    recused = 2
    accepted = 3


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
        "Users", foreign_keys=[user_sender_id], back_populates="trades_sended"
    )

    def __init__(
        self,
        user_sender_id,
        user_receiver_id,
        sticker_sender_id,
        sticker_receiver_id,
        status=1,
    ) -> None:
        self.user_sender_id = user_sender_id
        self.user_receiver_id = user_receiver_id
        self.sticker_sender_id = sticker_sender_id
        self.sticker_receiver_id = sticker_receiver_id
        self.status = status


def create_db(con):
    Base.metadata.create_all(con)
