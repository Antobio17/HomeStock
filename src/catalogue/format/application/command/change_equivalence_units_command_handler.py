
from dataclasses import dataclass
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.catalogue.format.domain.model.format_repository import FormatRepository
from src.catalogue.format.application.command.change_equivalence_units_command import ChangeEquivalenceUnitsCommand
from src.catalogue.format.domain.exception.change_equivalence_units_exception import ChangeEquivalenceUnitsException

@dataclass
class ChangeEquivalenceUnitsCommandHandler:
    __format_repository: FormatRepository
    __message_publisher: MessagePublisher

    def handle(self, command: ChangeEquivalenceUnitsCommand):
        format = self.__format_repository.find_by_id(command.id)
        if format is None:
            raise ChangeEquivalenceUnitsException(
                f'Format with ID {command.id} not found'
                f'formatWithID{command.id}NotFound'
            )
            
        format.change_equivalence_units(
            command.recipe_unit,
            command.storage_unit,
            command.storage_unit_equivalence,
            command.purchase_unit,
            command.purchase_unit_equivalence,
            command.purchase_price
        )
        
        self.__format_repository.save(format)
        for event in format.pull_domain_events():
            self.__message_publisher.execute(event)