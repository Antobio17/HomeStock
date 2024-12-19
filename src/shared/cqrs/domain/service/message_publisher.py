from dataclasses import dataclass, field
from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.message_broker.domain.service.producer import Producer

@dataclass
class MessagePublisher():
    __producer: Producer
    __publish_instantly: bool = True
    __messages: list[Message] = field(default_factory=list)
    
    def execute(self, message: Message) -> None:
        if not self.__publish_instantly:
            self.__messages.append(message)
            return
        
        print('Publishing one message...')
    
    def flush(self) -> None:
        for message in self.__messages:
            print('Publishing message...')
        
    def disable_publish_instantly(self) -> None:
        self.__publish_instantly = False
        