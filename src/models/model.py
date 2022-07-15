import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.getenv('DB_USER', 'postgres')
host = os.getenv('DB_HOST', 'localhost')
password = os.getenv('DB_PASSWORD', '123')
database = os.getenv('DB_NAME', 'authorization')
port = os.getenv('DB_PORT', '5432')

engine = create_engine(f"postgresql+pg8000://{user}:{password}@{host}:{port}/{database}", echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id: int
    name: str
    password: str

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    password = Column(String(4))

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return "Users(id='%s')" % self.id


Base.metadata.create_all(engine)
