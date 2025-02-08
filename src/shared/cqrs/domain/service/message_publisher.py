import json
import uuid
from dataclasses import dataclass, field
from src.shared.cqrs.domain.service.dto.message import Message
from src.shared.cqrs.domain.service.dto.metadata import Metadata
from src.shared.message_broker.domain.service.producer import Producer

@dataclass
class MessagePublisher():
    __producer: Producer
    __publish_instantly: bool = True
    __messages: list[Message] = field(default_factory=list)
    
    def execute(self, message: Message, headers: dict = {}, to_delay: bool = False) -> None:
        if not self.__publish_instantly:
            self.__messages.append(message)
            return
                
        dict = message.__dict__
        
        self.__producer.publish(
            message = json.dumps(dict, default=str),
            headers = headers,
            to_delay = to_delay,
            routing_key = message.get_name()
        )
    
    def flush(self, metadata: Metadata = None) -> None:
        self.__publish_instantly = True
        if metadata is None:
            metadata = Metadata(
                message_id = str(uuid.uuid4()),
                causation_id = str(uuid.uuid4()),
                correlation_id = str(uuid.uuid4())
            )
         
        for message in self.__messages:
            self.execute(
                message, 
                {
                    'message_id': metadata.message_id,
                    'correlation_id': metadata.correlation_id,
                    'causation_id': metadata.causation_id,
                }
            )
            
        self.__messages.clear()
        
    def disable_publish_instantly(self) -> None:
        self.__publish_instantly = False
        