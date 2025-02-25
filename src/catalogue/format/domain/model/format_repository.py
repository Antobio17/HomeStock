from typing import Union
from abc import ABC, abstractmethod
from src.catalogue.format.domain.model.format import Format

class FormatRepository(ABC):

    @abstractmethod
    def find_by_id(self, id: str) -> Union[Format, None]:
        pass

    @abstractmethod
    def save(self, format: Format)  -> None:
        pass