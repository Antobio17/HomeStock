from abc import ABC, abstractmethod

class SubmitTicketNeedleDataQuery(ABC):
    
    @abstractmethod
    def ticket_exists(self, reference: str) -> bool:
        pass