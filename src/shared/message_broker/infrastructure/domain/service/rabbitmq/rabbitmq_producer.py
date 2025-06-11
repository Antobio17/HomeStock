from src import thread_local
from dataclasses import dataclass
from src.shared.message_broker.domain.service.producer import Producer
from src.shared.message_broker.domain.connection.connection import Connection

@dataclass
class RabbitmqProducer(Producer):
    __connection: Connection
        
    def publish(
        self, 
        message: str,
        headers: dict = None,
        to_delay: bool = False,
        routing_key: str = '',
    ) -> None:
        if headers is None:
            headers = {}
        headers['schema_name'] = thread_local.schema_name
        
        self.__connection.publish_message(
            exchange = RabbitmqProducer.__exchange_name(routing_key, to_delay),
            routing_key = routing_key,
            headers = headers,
            properties = {},
            body = message
        )
        
    @staticmethod
    def __exchange_name(routing_key: str, to_delay: bool) -> str:
        parts = routing_key.split('.')
        if len(parts) < 6:
            raise ValueError(
                f'Routing key {routing_key} is malformed. ' + 
                'Correct format: <app>.<context>.<version>.<subcontext>.<message_type>.<action>'
            )
                        
        return parts[1] + '-delay' if to_delay else parts[1]
