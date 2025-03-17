from abc import ABC, abstractmethod
from src.purchase.ticket.domain.service.dto.ticket_extractor_result import TicketExtractorResult

class TicketExtractorService(ABC):
    
    @abstractmethod
    def execute(self, file_path: str) -> TicketExtractorResult:
        pass