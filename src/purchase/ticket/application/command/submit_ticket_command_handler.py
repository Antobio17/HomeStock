from dataclasses import dataclass
from src.purchase.ticket.domain.model.ticket import Ticket
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.shared.cqrs.application.command.command_handler import CommandHandler
from src.purchase.ticket.domain.model.ticket_repository import TicketRepository
from src.purchase.ticket.application.command.submit_ticket_command import SubmitTicketCommand
from src.purchase.ticket.domain.exception.submit_ticket_exception import SubmitTicketException
from src.purchase.ticket.domain.query_model.submit_ticket_needle_data_query import SubmitTicketNeedleDataQuery

@dataclass
class SubmitTicketCommandHandler(CommandHandler):
    __needle_data_query: SubmitTicketNeedleDataQuery
    __ticket_repository: TicketRepository
    __message_publisher: MessagePublisher
    
    def handle(self, command: SubmitTicketCommand):
        if self.__needle_data_query.ticket_exists(command.reference):
            raise SubmitTicketException(
                f'Ticket with reference {command.reference} already submitted',
                f'ticketWithReference{command.reference}AlreadySubmitted'
            )

        items = []
        for item in command.items:
            items.append(
                {
                    'description': item.description,
                    'quantity': item.quantity,
                    'amount': item.amount,
                }
            )
        
        ticket = Ticket.submit(
            command.supermarket,
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