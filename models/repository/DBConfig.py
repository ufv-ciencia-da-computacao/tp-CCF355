import sqlalchemy
from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker


@dataclass
class AlbumCredentials:
    host = "db1"


class DBConfig:
    host = None

    def __init__(self, host) -> None:
        self.host = host

        self.connection = sqlalchemy.create_engine(
            self.get_uri(), encoding="UTF-8", connect_args={"check_same_thread": False}
        )

    def get_uri(self):
        return f"sqlite:///{self.host}"


class SQLiteConnection:
    connection = {}
    session = {}

    @classmethod
    def get_connection(cls, host):
        db_key = f"{host}"

        if db_key not in cls.connection:
            config = DBConfig(host)
            cls.connection[db_key] = config.connection
            cls.session[db_key] = sessionmaker(config.connection)

        return cls.connection[db_key]
