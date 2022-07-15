from models.db_interface import DBInterface
from .posgres_db import Postgres


class Repository:
    db: DBInterface = None

    @staticmethod
    def connect() -> DBInterface:
        if Repository.db is None:
            Repository.db = Postgres()
        return Repository.db
