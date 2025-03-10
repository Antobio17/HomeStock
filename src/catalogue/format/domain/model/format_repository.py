from typing import Optional
from abc import ABC, abstractmethod
from src.catalogue.format.domain.model.format import Format

class FormatRepository(ABC):

    @abstractmethod
    def find_by_id(self, format_id: str) -> Optional[Format]:
        pass

    @abstractmethod
    def save(self, fmt: Format) -> None:
        pass