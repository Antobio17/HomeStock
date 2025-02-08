from typing import Union
from dataclasses import dataclass

@dataclass
class QueryResult:
    result: Union[list, dict]
    page: int
    page_size: int
    total: int