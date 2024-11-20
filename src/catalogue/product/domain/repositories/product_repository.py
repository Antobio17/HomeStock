
from abc import ABC, abstractmethod

class ProductRepository(ABC):

    @abstractmethod
    def findById(self, id: str):
        pass

    @abstractmethod
    def findAll(self):
        pass

    @abstractmethod
    def save(self, product):
        pass