from typing import Union
from dataclasses import dataclass
from src.catalogue.format.domain.model.format import Format
from src.catalogue.format.domain.model.format_repository import FormatRepository

@dataclass
class InMemoryFormatRepository(FormatRepository):
    product: Format = None
    saved: Format = None

    def find_by_id(self, id: str) -> Union[Format, None]:
        if self.product == None or self.product.id != id:
            return None
        return self.product

    def save(self, product: Format) -> None:
        self.saved = product
        
    def spy(self) -> Format:
        return self.saved
    
    def will_return(self, product: Format) -> None:
        self.product = product
