import json
from src import thread_local
from dataclasses import dataclass, field
from pika.spec import Basic, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from src.shared.logger.domain.service.logger_service import LoggerService
from src.shared.message_broker.domain.connection.connection import Connection
from src.shared.cqrs.application.dispatcher.message_dispatcher import MessageDispatcher
from src.shared.service_container.domain.service.service_container import ServiceContainer
from pika.exceptions import ConnectionClosedByBroker, AMQPChannelError, AMQPConnectionError
from src.shared.message_broker.infrastructure.domain.connection.rabbitmq.rabbitmq_connection import RabbitmqConnection

@dataclass
class RabbitmqConsumer:
    __exchange: str
    __queue_name: str
    __message_dispatcher: MessageDispatcher = field(default_factory = lambda: MessageDispatcher())
    __service_container: ServiceContainer = field(default_factory = lambda: ServiceContainer())

    @property
    def __rabbitmq_connection(self) -> RabbitmqConnection:
        return self.__service_container.get(Connection.__module__)
    
    @property
    def __logger(self) -> LoggerService:
        return self.__service_container.get(LoggerService.__module__)
        
    def __send_to_delay_queue(self, routing_key: str, headers: dict, body: str) -> None:
        retries = headers.get('retries', 0)
        retries = retries + 1
        
        if retries > 5:
            self.__send_to_failure_queue(routing_key, headers, body)
            return
        
        headers['retries'] = retries
        self.__rabbitmq_connection.publish_message(
            self.__exchange + '-delay',
            routing_key,
            headers,
            {'expiration': str(retries * 5000)},
            body,
        )
        
    def __send_to_failure_queue(self, routing_key: str, headers: dict, body: str) -> None:
        self.__rabbitmq_connection.publish_message(
            self.__exchange + '-failure',
            routing_key,
            headers,
            {},
            body
        )
    
    def on_message_callback(
        self,
        ch: BlockingChannel, 
        method: Basic.Deliver, 
        properties: BasicProperties, 
        body: bytes
    ) -> None:
        schema_name = properties.headers.get('schema_name', None)
        routing_key = method.routing_key
        body = body.decode('utf-8')
        if schema_name is None or routing_key is None:
            self.__send_to_failure_queue(routing_key, properties.headers, body)
            ch.basic_ack(method.delivery_tag)
            return

        try:
            thread_local.schema_name = schema_name
            self.__message_dispatcher.execute(routing_key, json.loads(body))
            ch.basic_ack(method.delivery_tag)
        except Exception:
            self.__send_to_delay_queue(routing_key, properties.headers, body)
            ch.basic_ack(method.delivery_tag)
        
    def execute(self) -> None:
        while True:
            try:
                self.__rabbitmq_connection.start_consuming(
                    queue_name = self.__queue_name,
                    callback = self.on_message_callback
                )
            except ConnectionClosedByBroker as e:
                self.__logger.error(f'Connection closed by broker: {e}')
                break
            except AMQPChannelError as e:
                self.__logger.error(f'AMQP channel error: {e}')
                break
            except AMQPConnectionError as e:
                self.__logger.error(f'AMQP connection error: {e}')
                self.__rabbitmq_connection.close()
                continue