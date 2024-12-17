from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.message_broker.domain.service.producer import Producer
from src.shared.message_broker.infrastructure.domain.connection.rabbitmq.rabbitmq_connection import RabbitmqConnection

class RabbitmqProducer(Producer):
    def __init__(self):
        self.__connection = RabbitmqConnection()
        
    def publish(self, message: Message) -> None:
        with self.__connection.channel() as channel:
            channel.basic_publish(
                exchange=self._exchange,
                routing_key=self._routing_key,
                body=message.serialize(),
            )