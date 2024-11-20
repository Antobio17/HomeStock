from abc import ABC, abstractmethod
from typing import TypeVar, Generic

R = TypeVar('R')  # For Repositories
S = TypeVar('S')  # For Services
Q = TypeVar('Q')  # For Query Models

class DependencyInjector(ABC, Generic[R, S, Q]):
    
    @abstractmethod
    def getRepository(self, repository: type[R]) -> R:
        pass
    
    @abstractmethod
    def getService(self, key: type[S]) -> S:
        pass
    
    @abstractmethod
    def getQueryModel(self, key: type[Q]) -> Q:
        pass