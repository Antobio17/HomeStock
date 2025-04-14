from dataclasses import dataclass

from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.shared.cqrs.application.command.command_handler import CommandHandler
from src.purchase.ticket.domain.model.ticket_repository import TicketRepository
from src.purchase.ticket.application.command.finish_ticket_validation_command import FinishTicketValidationCommand
from src.purchase.ticket.domain.exception.finish_ticket_validation_exception import FinishTicketValidationException
from src.purchase.ticket.domain.query_model.finish_ticket_validation_needle_data_query import FinishTicketValidationNeedleDataQuery

@dataclass
class FinishTicketValidationCommandHandler(CommandHandler):
    __needle_data_query: FinishTicketValidationNeedleDataQuery
    __ticket_repository: TicketRepository
    __message_publisher: MessagePublisher
    
    def handle(self, command: FinishTicketValidationCommand):
        ticket = self.__ticket_repository.find_by_id(command.ticket_id)
        if ticket is None:
            raise FinishTicketValidationException(
                f'Ticket with id {command.ticket_id} does not found',
                f'ticketWithId{command.ticket_id}DoesNotFound'
            )
        
        formats_index_by_item_id = {}
        for item in command.items:
            formats_index_by_item_id[item.ticket_item_id] = item.format_id
        
        format_ids = list(formats_index_by_item_id.values())
        if not self.__needle_data_query.all_formats_exist(format_ids):
            raise FinishTicketValidationException(
                f'Not all format ids passed exist',
                f'NotAllFormatIdsPassedExist'
            )
        
        ticket.finish_validation(
            formats_index_by_item_id
        )
        
        self.__ticket_repository.save(ticket)
        for event in ticket.pull_domain_events():
            self.__message_publisher.execute(event)