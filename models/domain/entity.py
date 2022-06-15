from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from ..repository.DBConfig import SQLiteConnection, AlbumCredentials

Base = declarative_base()

class User(Base):
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


class ListStickers(Base):
    __tablename__ = "list_stickers"
    
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    sticker_id = Column(ForeignKey("stickers.id"), primary_key=True)
    count = Column(Integer)

    def __init__(self, user_id: int, sticker_id: int, count: int):
        self.user_id = user_id
        self.sticker_id = sticker_id
        self.count = count

def create_db(con):
    Base.metadata.create_all(con)

def populate_db():
    pass
