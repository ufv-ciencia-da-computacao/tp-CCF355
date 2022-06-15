import sqlalchemy
from dataclasses import dataclass


@dataclass
class AlbumCredentials:
    host = "db1"


class DBConfig:
    host = None

    def __init__(self, host) -> None:
        self.host = host

        self.connection = sqlalchemy.create_engine(self.get_uri(), encoding="UTF-8")

    def get_uri(self):
        return f"sqlite:///{self.host}"


class SQLiteConnection:
    connection = {}

    @classmethod
    def get_connection(cls, host):
        db_key = f"{host}"

        if db_key not in cls.connection:
            cls.connection[db_key] = DBConfig(host).connection

        return cls.connection[db_key]