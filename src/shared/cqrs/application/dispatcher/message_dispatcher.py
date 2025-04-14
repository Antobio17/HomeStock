import glob
import yaml
from dataclasses import dataclass, field
from src.shared.cqrs.domain.service.domain_event_hydrator import DomainEventHydrator
from src.shared.service_container.domain.service.service_container import ServiceContainer

@dataclass
class MessageDispatcher:
    __service_container: ServiceContainer = field(default_factory = lambda: ServiceContainer())
    __subscribers: list[str] = field(default_factory = list)
    
    def __suscribe_event(self, event_name: str) -> None:
        pattern = 'src/*/*/infrastructure/application/subscribers.yaml'
        for yaml_path in glob.glob(pattern):
            with open(yaml_path, 'r') as file:
                config = yaml.safe_load(file)
                
            if 'services' not in config:
                raise KeyError(f'The \'services\' key not found in YAML file: {yaml_path}')
            for key, subscriber in config['services'].items():
                if subscriber['event_name'] != event_name:
                    continue
                
                self.__subscribers.append(key)
    
    def __dispatch_event(self, routing_key: str, body: dict) -> None:
        self.__suscribe_event(routing_key)
        if len(self.__subscribers) == 0:
            return
        
        hydrated_event = DomainEventHydrator.execute(routing_key, body)
        for key in self.__subscribers:
            subscriber = self.__service_container.get(key)

            try:
                subscriber.handle(hydrated_event)
            except Exception as e:
                print(e)
                pass
            
            self.__service_container.clear()
            self.__subscribers = []
            
                  
    def execute(self, routing_key: str, body: dict):
        if 'event' not in routing_key and 'command' not in routing_key:
            raise ValueError(f'Substring event or command not found in {routing_key}')
        
        self.__dispatch_event(routing_key, body) if 'event' in routing_key else None
        # TODO self.__dispatch_command(routing_key, body) if 'command' in routing_key else None
