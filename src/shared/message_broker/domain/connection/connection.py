from abc import ABC, abstractmethod

class Connection(ABC):
    
    @abstractmethod
    def start_consuming(self, queue_name: str, callback: callable, auto_ack: bool = True):
        pass
    
    @abstractmethod
    def publish_message(self, exchange: str, routing_key: str, headers: dict, body: str):
        pass
