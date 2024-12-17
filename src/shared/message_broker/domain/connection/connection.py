from abc import ABC, abstractmethod

class Connection(ABC):
    
    @property
    @abstractmethod
    def connection(self):
        pass
