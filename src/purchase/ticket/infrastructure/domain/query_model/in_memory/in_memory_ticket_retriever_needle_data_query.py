from typing import Optional
from src.purchase.ticket.domain.query_model.ticket_retriever_needle_data_query import TicketRetrieverNeedleDataQuery

class InMemoryTicketRetrieverNeedleDataQuery(TicketRetrieverNeedleDataQuery):
    __ticket_pool: dict
    
    def get_ticket_pool(self, supermarket: str) -> Optional[str]:
        return self.__ticket_pool[supermarket]