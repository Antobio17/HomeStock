from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.message_broker.domain.service.producer import Producer

class RabbitmqProducer(Producer):

    def publish(self, message: Message) -> None:
        with self._connection.channel() as channel:
            channel.basic_publish(
                exchange=self._exchange,
                routing_key=self._routing_key,
                body=message.serialize(),
            )