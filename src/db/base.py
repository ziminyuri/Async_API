from abc import ABC, abstractmethod

from services.es_parser import PARAMS_TYPE


class AbstractRepository(ABC):
    """Абстрактный клас для базы данных"""

    @abstractmethod
    def get(self, index: str, id_: str):
        pass

    @abstractmethod
    def search(self, index: str, params: PARAMS_TYPE):
        pass

    @abstractmethod
    def close(self):
        pass
