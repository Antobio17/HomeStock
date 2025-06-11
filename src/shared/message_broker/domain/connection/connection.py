from abc import ABC, abstractmethod

class Connection(ABC):
    
    @abstractmethod
    def start_consuming(self, queue_name: str, callback: callable, auto_ack: bool = False):
        pass
    
    @abstractmethod
    def publish_message(
        self, 
        exchange: str, 
        routing_key: str, 
        headers: dict, 
        properties: dict, 
        body: str
    ):
        pass
    
    @abstractmethod
    def exchange_declare(
        self, 
        exchange: str, 
        exchange_type: str,
        durable: bool = True, 
        auto_delete: bool = False,
        arguments: dict = None
    ):
        pass
    
    @abstractmethod
    def queue_declare(
        self, 
        queue: str, 
        arguments: dict,
        durable: bool = True, 
        auto_delete: bool = False,
        exclusive: bool = False,
    ):
        pass
    
    @abstractmethod
    def queue_bind(
        self, 
        queue: str, 
        exchange: str, 
        routing_key: str,
        arguments: dict = None
    ):
        pass
    
    @abstractmethod
    def close(self) -> None:
        pass
