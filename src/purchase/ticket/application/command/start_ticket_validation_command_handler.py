from dataclasses import dataclass

from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.shared.cqrs.application.command.command_handler import CommandHandler
from src.purchase.ticket.domain.model.ticket_repository import TicketRepository
from src.purchase.ticket.application.command.start_ticket_validation_command import StartTicketValidationCommand
from src.purchase.ticket.domain.exception.start_ticket_validation_exception import StartTicketValidationException
from src.purchase.ticket.domain.query_model.start_ticket_validation_needle_data_query import StartTicketValidationNeedleDataQuery

@dataclass
class StartTicketValidationCommandHandler(CommandHandler):
    __needle_data_query: StartTicketValidationNeedleDataQuery
    __ticket_repository: TicketRepository
    __message_publisher: MessagePublisher
    
    def handle(self, command: StartTicketValidationCommand):
        ticket = self.__ticket_repository.find_by_id(command.ticket_id)
        if ticket is None:
            raise StartTicketValidationException(
                f'Ticket with id {command.ticket_id} does not found',
                f'ticketWithId{command.ticket_id}DoesNotFound'
            )
        
        items = []
        format_ids = []
        product_ids = []
        for item in command.items:
            product_ids.append(item.product_id)
            None if item.format_id is None else format_ids.append(item.format_id)
            items.append(
                {
                    'description': item.description,
                    'quantity': item.quantity,
                    'amount': item.amount,
                    'format_id': item.format_id,
                    'product_id': item.product_id
                }
            )
        
        product_ids = list(set(product_ids))
        if not self.__needle_data_query.all_products_exist(product_ids):
            raise StartTicketValidationException(
                f'Not all product ids passed exist',
                f'NotAllProductIdsPassedExist'
            )
        format_ids = list(set(format_ids))
        if not self.__needle_data_query.all_formats_exist(format_ids):
            raise StartTicketValidationException(
                f'Not all format ids passed exist',
                f'NotAllFormatIdsPassedExist'
            )
        
        ticket.start_validation(
            command.reference,
            command.subtotal,   
            command.discount_amount,
            command.taxes,
            command.tax_amount,
            command.total,
            command.purchased_at,
            items
        )
        
        self.__ticket_repository.save(ticket)
        for event in ticket.pull_domain_events():
            self.__message_publisher.execute(event)