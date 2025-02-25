from dataclasses import dataclass
from src.catalogue.format.domain.query_model.create_format_needle_data_query import CreateFormatNeedleDataQuery

@dataclass
class InMemoryCreateFormatNeedleDataQuery(CreateFormatNeedleDataQuery):
    
    def product_exists(self, product_id: str) -> bool:
        return []