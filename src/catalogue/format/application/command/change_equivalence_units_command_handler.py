
from dataclasses import dataclass
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.shared.cqrs.application.command.command_handler import CommandHandler
from src.catalogue.format.domain.model.format_repository import FormatRepository
from src.catalogue.format.application.command.change_equivalence_units_command import ChangeEquivalenceUnitsCommand
from src.catalogue.format.domain.exception.change_equivalence_units_exception import ChangeEquivalenceUnitsException

@dataclass
class ChangeEquivalenceUnitsCommandHandler(CommandHandler):
    __format_repository: FormatRepository
    __message_publisher: MessagePublisher

    def handle(self, command: ChangeEquivalenceUnitsCommand):
        fmt = self.__format_repository.find_by_id(command.id)
        if fmt is None:
            raise ChangeEquivalenceUnitsException(
                f'Format with ID {command.id} not found',
                f'formatWithID{command.id}NotFound'
            )
            
        fmt.change_equivalence_units(
            command.recipe_unit,
            command.storage_unit,
            command.storage_unit_equivalence,
            command.purchase_unit,
            command.purchase_unit_equivalence,
            command.purchase_price
        )
        
        self.__format_repository.save(fmt)
        for event in fmt.pull_domain_events():
            self.__message_publisher.execute(event)