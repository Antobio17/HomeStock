from abc import ABC, abstractmethod

class Producer(ABC):

    @abstractmethod
    def publish(
        self, 
        message: str,
        headers: dict = {},
        to_delay: bool = False,
        routing_key: str = '',
    ) -> None:
        pass