import requests
from datetime import datetime, UTC
from dataclasses import dataclass
from src.shared.logger.domain.service.logger_service import LoggerService

@dataclass
class ElasticsearchLoggerService(LoggerService):
    __url: str
    __prefix_index_name: str

    def error(self, message: str) -> None:
        self.__log(self.LEVEL_ERROR, message)

    def warning(self, message: str) -> None:
        self.__log(self.LEVEL_WARNING, message)

    def info(self, message: str) -> None:
        self.__log(self.LEVEL_INFO, message)

    def debug(self, message: str) -> None:
        self.__log(self.LEVEL_DEBUG, message)

    def __log(self, level: str, message: str) -> None:
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            requests.post(
                f'{self.__url}/{self.__prefix_index_name}-{today}/_doc', 
                json = {
                    'timestamp': datetime.now(UTC).isoformat(),
                    'level': level,
                    'message': message,
                }
            )
        except requests.exceptions.ConnectionError:
            pass