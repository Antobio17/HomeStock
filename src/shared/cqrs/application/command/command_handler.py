from abc import ABC, abstractmethod

class CommandHandler(ABC):

    def __init__(self, *args, **kwargs):
        pass        
        
    @abstractmethod
    def handle(self, command) -> None:
        pass