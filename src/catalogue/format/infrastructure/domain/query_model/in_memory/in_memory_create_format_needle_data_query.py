from dataclasses import dataclass
from src.catalogue.format.domain.query_model.create_format_needle_data_query import CreateFormatNeedleDataQuery

class InMemoryCreateFormatNeedleDataQuery(CreateFormatNeedleDataQuery):
    __product_exists: bool
    
    def product_exists(self, product_id: str) -> bool:
        return self.__product_exists
    
    def will_return(self, product_exists: bool):
        self.__product_exists = product_exists