from typing import Union
from abc import ABC, abstractmethod

class ProductRepository(ABC):

    @abstractmethod
    def find_by_id(self, id: str) -> Union[object, None]:
        pass

    @abstractmethod
    def save(self, product)  -> None:
        pass