from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command import Command
from src.shared.cqrs.application.middleware.middleware import Middleware
from src.shared.service_container.domain.service.service_container import ServiceContainer
from src.shared.cqrs.application.middleware.transaction_middleware import TransactionMiddleware
from src.shared.cqrs.application.middleware.message_publisher_middleware import MessagePublisherMiddleware
 
@dataclass
class CommandBus():
    __container: ServiceContainer = field(default_factory=lambda: ServiceContainer())

    def middlewares(self) -> list[Middleware]:
        return [
            MessagePublisherMiddleware(
                self.__container.message_publisher, 
                self.__container.metadata
            ),
            TransactionMiddleware(self.__container.transaction_manager),
        ]
        
    def __get_handler_module(self, command: Command) -> str:
        context = command.__module__.split(".")[1]
        subcontext = command.__module__.split(".")[2]
        command_name = type(command).__name__
        command_name_snake_case = ''.join(['_' + i.lower() if i.isupper() else i for i in command_name]).lstrip('_')
        return f'src.{context}.{subcontext}.application.command.' + command_name_snake_case + '_handler'
    
    def handle(self, command: Command) -> None:
        handler_class = self.__get_handler_module(command)
        command_handler = self.__container.get(handler_class)
        
        for middleware in self.middlewares():
            middleware.before_handle()
            
        command_handler.handle(command)
        
        for middleware in reversed(self.middlewares()):
            middleware.after_handle()
                
