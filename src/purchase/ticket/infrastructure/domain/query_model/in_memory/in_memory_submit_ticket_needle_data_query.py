from src.purchase.ticket.domain.query_model.submit_ticket_needle_data_query import SubmitTicketNeedleDataQuery

class InMemorySubmitTicketNeedleDataQuery(SubmitTicketNeedleDataQuery):
    __ticket_exists: bool = False
    
    def ticket_exists(self, reference: str) -> bool:
        return self.__ticket_exists
    
    def will_return(self, __ticket_exists: bool):
        self.__ticket_exists = __ticket_exists