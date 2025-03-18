from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.service_container.domain.service.service_container import ServiceContainer
from src.purchase.ticket.application.command.dto.submit_ticket_item import SubmitTicketItem
from src.purchase.ticket.application.command.submit_ticket_command import SubmitTicketCommand
from src.purchase.ticket.domain.service.ticket_retriever_service import TicketRetrieverService
from src.purchase.ticket.domain.exception.submit_ticket_exception import SubmitTicketException
from src.purchase.ticket.domain.service.ticket_extractor_service import TicketExtractorService
from src.purchase.ticket.domain.service.dto.ticket_extractor_result import TicketExtractorResult
from src.shared.database.infrastructure.adapter.cli.sqlalchemy_multitenant_connection_cli import SqlalchemyMultitenantConnectionCli

class SubmitMercadonaTicketFromInboxCli(SqlalchemyMultitenantConnectionCli):
    
    def __init__(self):
        self.__command_bus = CommandBus()
        self.__service_container = ServiceContainer()
        
    @property
    def __ticket_extractor_service(self) -> TicketExtractorService:
        return self.__service_container.get('src.purchase.ticket.domain.service.ticket_extractor_service_mercadona')
        
    @property
    def __ticket_retriever_service(self) -> TicketRetrieverService:
        return self.__service_container.get('src.purchase.ticket.domain.service.ticket_retriever_service_mercadona')
        
    def execute(self) -> None:
        while True:
            file = self.__ticket_retriever_service.execute()
            if file is None:
                break
            
            ticket = self.__ticket_extractor_service.execute(file)
            try:
                self.__command_bus.handle(self.__get_command(ticket))
            except SubmitTicketException as e:
                print('Exception: ' + e.message)
    
    @staticmethod
    def __get_command(ticket: TicketExtractorResult) -> SubmitTicketCommand:
        items = []
        for item in ticket.items:
            items.append(
                SubmitTicketItem(
                    item.description,
                    item.quantity,
                    item.amount
                )
            )
        
        return SubmitTicketCommand(
            ticket.supermarket,
            ticket.reference,
            ticket.subtotal,
            ticket.discount_amount,
            ticket.taxes,
            ticket.tax_amount,
            ticket.total,
            ticket.purchased_at,
            items
        )       
                
    
if __name__ == '__main__':
    SubmitMercadonaTicketFromInboxCli().execute_multitenant()