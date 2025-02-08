import os
import pika # type: ignore
from dataclasses import dataclass
from src.shared.message_broker.domain.connection.connection import Connection

@dataclass
class RabbitmqConnection(Connection):
    __username: str
    __password: str
    __host: str
    __port: str
    __vhost: str
    __connection = None
    
    
    @property
    def __connect(self):
        if self.__connection is None:
            credentials = pika.PlainCredentials(
                username = self.__username,
                password = self.__password                                   
            )
            self.__connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host = self.__host,
                    port = self.__port,
                    virtual_host = self.__vhost,
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