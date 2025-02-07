from typing import Union
from dataclasses import dataclass

@dataclass
class QueryResult:
    result: Union[list, dict]
    page: int
    pageSize: int
    total: int