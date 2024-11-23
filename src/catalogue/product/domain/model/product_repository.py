from abc import ABC, abstractmethod

class ProductRepository(ABC):

    @abstractmethod
    def find_by_id(self, id: str):
        pass

    @abstractmethod
    def save(self, product):
        pass