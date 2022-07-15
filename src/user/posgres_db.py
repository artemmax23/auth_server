from models.db_interface import DBInterface
from models.model import Session, Users


class Postgres(DBInterface):
    session = Session()

    def get(self, name: str) -> Users:
        return self.session.query(Users).filter(Users.name == name).first()
