from abc import ABC, abstractmethod
from src.shared.cqrs.application.query.query import Query
from src.shared.cqrs.application.query.dto.query_result import QueryResult

class QueryHandler(ABC):

    def __init__(self, *args, **kwargs):
        pass        
        
    @abstractmethod
    def handle(self, query: Query) -> QueryResult:
        pass