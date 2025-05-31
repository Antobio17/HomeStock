from abc import ABC, abstractmethod

class LoggerService(ABC):
    
    LEVEL_ERROR = 'ERROR'
    LEVEL_WARNING = 'WARNING'
    LEVEL_INFO = 'INFO'
    LEVEL_DEBUG = 'DEBUG'
    
    @abstractmethod
    def error(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        pass