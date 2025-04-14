from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.cqrs.application.subscriber.subscriber import Subscriber
from src.purchase.ticket.domain.model.ticket import STATUS_VALIDATION_IN_PROGRESS
from src.purchase.ticket.domain.event.ticket_validation_started import TicketValidationStarted
from src.catalogue.format.application.command.create_format_command import CreateFormatCommand
from src.purchase.ticket.domain.exception.validate_ticket_exception import ValidateTicketException
from src.purchase.ticket.application.command.dto.finish_ticket_validation_item import FinishTicketValidationItem
from src.purchase.ticket.application.command.finish_ticket_validation_command import FinishTicketValidationCommand
from src.purchase.ticket.domain.query_model.validate_ticket_needle_data_query import ValidateTicketNeedleDataQuery

@dataclass
class ValidateTicketDueToTicketValidationStartedSubscriber(Subscriber):
    __validate_ticket_needle_data_query: ValidateTicketNeedleDataQuery 
    __command_bus: CommandBus = field(default_factory = lambda: CommandBus())
    
    def handle(self, event: TicketValidationStarted) -> None:
        format_names = []
        for item in event.items:
            if item.get('format_id', None) is not None:
                continue
            
            format_names.append(item['description'])
            self.__command_bus.handle(CreateFormatCommand(
                item['product_id'], 
                item['description']
            ))
        
        if len(format_names) == 0:
            self.__command_bus.handle(FinishTicketValidationCommand(
                ticket_id = event.aggregate_id, 
                items = []
            ))
            return    
        
        command_items = []
        formats = self.__validate_ticket_needle_data_query.formats(format_names)
        items = self.__validate_ticket_needle_data_query.items(event.aggregate_id)
        for item in items:
            format_id = formats.get(item['description'], None)
            if format_id is None:
                continue
            
            command_items.append(FinishTicketValidationItem(item['id'], format_id))
        
        self.__command_bus.handle(FinishTicketValidationCommand(
            event.aggregate_id, 
            command_items
        ))
        
        
