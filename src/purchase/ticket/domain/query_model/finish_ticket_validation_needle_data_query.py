from abc import ABC, abstractmethod

class FinishTicketValidationNeedleDataQuery(ABC):
    
    @abstractmethod
    def all_formats_exist(self, format_ids: list) -> bool:
        pass