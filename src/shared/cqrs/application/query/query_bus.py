from dataclasses import dataclass, field
from src.shared.cqrs.application.query.query import Query
from src.shared.service_container.domain.service.service_container import ServiceContainer
from src.shared.cqrs.application.query.dto.query_result import QueryResult

@dataclass
class QueryBus():
    __container: ServiceContainer = field(default_factory=lambda: ServiceContainer())
        
    def __get_handler_module(self, query: Query) -> str:
        context = query.__module__.split(".")[1]
        subcontext = query.__module__.split(".")[2]
        query_name = type(query).__name__
        query_name_snake_case = ''.join(['_' + i.lower() if i.isupper() else i for i in query_name]).lstrip('_')
        return f'src.{context}.{subcontext}.application.query.' + query_name_snake_case + '_handler'
    
    def handle(self, query: Query) -> QueryResult:
        handler_class = self.__get_handler_module(query)
        query_handler = self.__container.get(handler_class)
            
        return query_handler.handle(query)
                
