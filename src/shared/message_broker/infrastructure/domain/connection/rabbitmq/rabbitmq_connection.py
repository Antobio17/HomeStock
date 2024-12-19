import os
import pika
from dataclasses import dataclass
from src.shared.message_broker.domain.connection.connection import Connection

@dataclass
class RabbitmqConnection(Connection):
    __connection = None
    
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
                    virtual_host = os.getenv('RABBITMQ_VIRTUAL_HOST'),
                    credentials = credentials
                )
            )
            
        return self.__connection
    
    def start_consuming(self, queue_name: str, callback: callable, auto_ack: bool = True):
        channel = self.__connect().channel()
        channel.basic_consume(
            queue = queue_name,
            on_message_callback = callback,
            auto_ack = auto_ack
        )
        channel.start_consuming()
    
    def publish_message(self, exchange: str, routing_key: str, headers: dict, body: str):
        channel = self.__connect().channel()
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