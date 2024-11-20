from typing import cast

from src.shared.cqrs.application.command import Command
from src.shared.cqrs.application.command_handler import CommandHandler


class CommandBus():
    
    def __get_dependency_injector(self, command: Command):
        context = command.__module__.split(".")[1]
        subcontext = command.__module__.split(".")[2]
        module_path = f'src.{context}.{subcontext}.infrastructure.domain.dependency_injector'
        dependency_injector_module = __import__(module_path, fromlist=['DependencyInjector'])
        subcontext_camel_case = ''.join(word.capitalize() for word in subcontext.split('_'))
    
        return getattr(dependency_injector_module, subcontext_camel_case + 'DependencyInjector')()
    
    def __get_handler_class(self, command: Command):
        context = command.__module__.split(".")[1]
        subcontext = command.__module__.split(".")[2]
        command_name = type(command).__name__
        command_name_snake_case = ''.join(['_' + i.lower() if i.isupper() else i for i in command_name]).lstrip('_')
        handler_module_path = f'src.{context}.{subcontext}.application.use_cases.' + command_name_snake_case + '_handler'
        handler_module = __import__(handler_module_path, fromlist=[command_name + 'Handler'])
        
        return getattr(handler_module, command_name + 'Handler')
    
    
    def handle(self, command: Command) -> None:
        dependency_injector = self.__get_dependency_injector(command)
        handler_class = self.__get_handler_class(command)
        
        command_handler = handler_class(dependency_injector)
        command_handler = cast(CommandHandler, command_handler)
        command_handler.handle(command)
        
