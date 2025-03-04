from dataclasses import dataclass
from src.catalogue.format.domain.model.format import Format
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.shared.cqrs.application.command.command_handler import CommandHandler
from src.catalogue.format.domain.model.format_repository import FormatRepository
from src.catalogue.format.application.command.create_format_command import CreateFormatCommand
from src.catalogue.format.domain.exception.create_format_exception import CreateFormatException
from src.catalogue.format.domain.query_model.create_format_needle_data_query import CreateFormatNeedleDataQuery

@dataclass
class CreateFormatCommandHandler(CommandHandler):
    __needle_data_query: CreateFormatNeedleDataQuery
    __format_repository: FormatRepository
    __message_publisher: MessagePublisher

    def handle(self, command: CreateFormatCommand) -> None:
        if not self.__needle_data_query.product_exists(command.product_id):
            raise CreateFormatException(
                f'Product with ID {command.product_id} not found to assign format',
                f'productWithID{command.product_id}NotFoundToAssignFormat'
            )
            
        fmt = Format.create(command.product_id, command.name)
        
        self.__format_repository.save(fmt)
        for event in fmt.pull_domain_events():
            self.__message_publisher.execute(event)