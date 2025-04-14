import json
from src import thread_local
from dataclasses import dataclass, field
from pika.spec import Basic, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
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
        
    def __send_to_failure_queue(self, routing_key: str, headers: dict, body: str) -> None:
        self.__rabbitmq_connection.publish_message(
            self.__exchange + '-failure',
            routing_key,
            headers,
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

        thread_local.schema_name = schema_name
        self.__message_dispatcher.execute(routing_key, json.loads(body))
        
    def execute(self) -> None:
        while True:
            try:
                self.__rabbitmq_connection.start_consuming(
                    queue_name = self.__queue_name,
                    callback = self.on_message_callback
                )
            except ConnectionClosedByBroker as e:
                print(e)
                break
            except AMQPChannelError as e:
                print(e)
                break
            except AMQPConnectionError as e:
                print(e)
                self.__rabbitmq_connection.close()
                continue