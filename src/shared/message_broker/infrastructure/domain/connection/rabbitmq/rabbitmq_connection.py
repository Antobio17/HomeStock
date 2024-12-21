import os
import pika
from dataclasses import dataclass
from src.shared.message_broker.domain.connection.connection import Connection

@dataclass
class RabbitmqConnection(Connection):
    __connection = None
    
    
    @property
    def __connect(self):
        if self.__connection is None:
            credentials = pika.PlainCredentials(
                username = os.getenv('RABBITMQ_USER'),
                password = os.getenv('RABBITMQ_PASSWORD')                                   
            )
            self.__connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = os.getenv('RABBITMQ_HOST'),
                    port = os.getenv('RABBITMQ_PORT'),
                    virtual_host = os.getenv('RABBITMQ_VHOST'),
                    credentials = credentials
                )
            )
            
        return self.__connection
    
    def start_consuming(self, queue_name: str, callback: callable, auto_ack: bool = True):
        channel = self.__connect.channel()
        channel.basic_consume(
            queue = queue_name,
            on_message_callback = callback,
            auto_ack = auto_ack
        )
        channel.start_consuming()
    
    def publish_message(self, exchange: str, routing_key: str, headers: dict, body: str):
        channel = self.__connect.channel()
        channel.basic_publish(
            exchange = exchange,
            routing_key = routing_key,
            body = body,
            properties = pika.BasicProperties(
                headers = headers,
                delivery_mode = 2,
                content_type = 'text/plain'   
            ) 
        )
        channel.close()
        
    def exchange_declare(
        self, 
        exchange: str, 
        exchange_type: str,
        durable: bool = True, 
        auto_delete: bool = False
    ):
        channel = self.__connect.channel()
        channel.exchange_declare(
            exchange = exchange,
            exchange_type = exchange_type,
            durable = durable,
            auto_delete = auto_delete
        )
        channel.close()
        
    def queue_declare(
        self, 
        queue: str, 
        arguments: dict = {},
        durable: bool = True, 
        auto_delete: bool = False,
        exclusive: bool = False,
    ):
        channel = self.__connect.channel()
        channel.queue_declare(
            queue = queue,
            durable = durable,
            auto_delete = auto_delete,
            exclusive = exclusive,
            arguments = arguments
        )
        channel.close()
        
    def queue_bind(
        self, 
        queue: str, 
        exchange: str, 
        routing_key: str
    ):
        channel = self.__connect.channel()
        channel.queue_bind(
            queue = queue,
            exchange = exchange,
            routing_key = routing_key
        )
        channel.close()