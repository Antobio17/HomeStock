from abc import ABC, abstractmethod

class StartTicketValidationNeedleDataQuery(ABC):
    
    @abstractmethod
    def all_products_exist(self, product_ids: list) -> bool:
        pass
    
    @abstractmethod
    def all_formats_exist(self, format_ids: list) -> bool:
        pass