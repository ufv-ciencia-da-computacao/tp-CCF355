from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from ..repository.DBConfig import SQLiteConnection, AlbumCredentials

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    stickers = relationship(
        "Stickers", secondary="list_stickers", back_populates="users"
    )

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Stickers(Base):
    __tablename__ = 'stickers'

    id = Column(Integer, primary_key=True)
    playername = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    rarity = Column(Integer, nullable=False)
    # photo
    users = relationship(
        "Users", secondary="list_stickers", back_populates="stickers"
    )

    def __init__(self, playername: str, country: str, rarity: int):
        self.playername = playername
        self.country = country
        self.rarity = rarity

    def __repr__(self) -> str:
        return f"(id:{self.id}, playername: {self.playername}, country: {self.country}, rarity: {self.rarity})"


class ListStickers(Base):
    __tablename__ = "list_stickers"
    
    id = Column(Integer, primary_key=Integer)
    user_id = Column(ForeignKey("users.id"))
    sticker_id = Column(ForeignKey("stickers.id"))

    def __init__(self, user_id: int, sticker_id: int):
        self.user_id = user_id
        self.sticker_id = sticker_id


def create_db(con):
    Base.metadata.create_all(con)

