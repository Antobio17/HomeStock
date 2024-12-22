import json
from dataclasses import dataclass, field
from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.message_broker.domain.service.producer import Producer

@dataclass
class MessagePublisher():
    __producer: Producer
    __publish_instantly: bool = True
    __messages: list[Message] = field(default_factory=list)
    
    def execute(self, message: Message, to_delay: bool = False) -> None:
        if not self.__publish_instantly:
            self.__messages.append(message)
            return
                
        dict = message.__dict__
        
        self.__producer.publish(
            message = json.dumps(dict, default=str),
            headers = {},
            to_delay = to_delay,
            routing_key = message.routing_key
        )
    
    def flush(self) -> None:
        self.__publish_instantly = True
        for message in self.__messages:
            self.execute(message)
        
    def disable_publish_instantly(self) -> None:
        self.__publish_instantly = False
        