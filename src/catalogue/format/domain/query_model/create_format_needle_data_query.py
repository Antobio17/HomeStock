from abc import ABC, abstractmethod

class CreateFormatNeedleDataQuery(ABC):
    
    @abstractmethod
    def product_exists(self, product_id: str) -> bool:
        pass