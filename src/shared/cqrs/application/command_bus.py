from src.shared.cqrs.application.command import Command
from src.shared.cqrs.application.command_handler import CommandHandler
from src.shared.service_container.domain.service.service_container import ServiceContainer

class CommandBus():
    
    def __init__(self):
        self.container = ServiceContainer()

    
    def __get_handler_module(self, command: Command):
        context = command.__module__.split(".")[1]
        subcontext = command.__module__.split(".")[2]
        command_name = type(command).__name__
        command_name_snake_case = ''.join(['_' + i.lower() if i.isupper() else i for i in command_name]).lstrip('_')
        return f'src.{context}.{subcontext}.application.use_cases.' + command_name_snake_case + '_handler'
        
    
    def handle(self, command: Command) -> None:
        handler_class = self.__get_handler_module(command)
        command_handler = self.container.get(handler_class)
        command_handler.handle(command)
        
