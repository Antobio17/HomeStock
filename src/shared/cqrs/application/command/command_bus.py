from dataclasses import dataclass, field
from src.shared import service_container
from src.shared.cqrs.application.command.command import Command
from src.shared.service_container.infrastructure.domain.service.service_container import ServiceContainer

@dataclass
class CommandBus():
    container: ServiceContainer = field(default_factory=lambda: service_container)

    def __get_handler_module(self, command: Command):
        context = command.__module__.split(".")[1]
        subcontext = command.__module__.split(".")[2]
        command_name = type(command).__name__
        command_name_snake_case = ''.join(['_' + i.lower() if i.isupper() else i for i in command_name]).lstrip('_')
        return f'src.{context}.{subcontext}.application.command.' + command_name_snake_case + '_handler'
        
    
    def handle(self, command: Command) -> None:
        handler_class = self.__get_handler_module(command)
        command_handler = self.container.get(handler_class)
        command_handler.handle(command)
        
        self.container.get_writer_session().commit()
        
