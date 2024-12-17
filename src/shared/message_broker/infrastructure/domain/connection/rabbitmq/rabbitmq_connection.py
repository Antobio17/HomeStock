import os
import pika
from dataclasses import dataclass
from src.shared.message_broker.domain.connection.connection import Connection

@dataclass
class RabbitmqConnection(Connection):
    __connection = None
    
    @property
    def connection(self):
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