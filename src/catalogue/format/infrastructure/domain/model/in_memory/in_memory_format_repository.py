from typing import Union
from dataclasses import dataclass
from src.catalogue.format.domain.model.format import Format
from src.catalogue.format.domain.model.format_repository import FormatRepository

@dataclass
class InMemoryFormatRepository(FormatRepository):
    fmt: Format = None
    saved: Format = None

    def find_by_id(self, format_id: str) -> Union[Format, None]:
        if self.fmt is None or self.fmt.id != id:
            return None
        return self.fmt

    def save(self, fmt: Format) -> None:
        self.saved = fmt
        
    def spy(self) -> Format:
        return self.saved
    
    def will_return(self, fmt: Format) -> None:
        self.fmt = fmt
