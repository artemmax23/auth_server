from abc import ABC, abstractmethod
from models.model import Users


class DBInterface(ABC):

    @abstractmethod
    def get(self, name: str) -> Users:
        pass
