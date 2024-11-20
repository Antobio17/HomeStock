from abc import ABC, abstractmethod

from src.shared.dependency_injector.domain.dependendy_injector import DependencyInjector

class CommandHandler(ABC):

    def __init__(self, dependency_injector: DependencyInjector):
        pass        
        
    @abstractmethod
    def handle(self, command) -> None:
        pass