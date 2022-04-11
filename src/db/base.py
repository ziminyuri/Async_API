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


class AbstractStorage(ABC):
    """Абстрактный класс для кэширования данных"""

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, data):
        pass

    @abstractmethod
    def close(self):
        pass
