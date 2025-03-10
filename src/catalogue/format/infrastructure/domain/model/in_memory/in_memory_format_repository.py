from typing import Optional
from dataclasses import dataclass
from src.catalogue.format.domain.model.format import Format
from src.catalogue.format.domain.model.format_repository import FormatRepository

@dataclass
class InMemoryFormatRepository(FormatRepository):
    __fmt: Format = None
    __saved: Format = None

    def find_by_id(self, format_id: str) -> Optional[Format]:
        if self.__fmt is None or self.__fmt.id != format_id:
            return None
        return self.__fmt

    def save(self, fmt: Format) -> None:
        self.__saved = fmt
        
    def spy(self) -> Format:
        return self.__saved
    
    def will_return(self, fmt: Format) -> None:
        self.__fmt = fmt
