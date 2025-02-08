import os
import yaml # type: ignore
import uuid
from typing import Any, Dict, Union
from importlib import import_module
from dataclasses import dataclass, field
from src.shared.cqrs.domain.service.dto.metadata import Metadata
from src.shared.cqrs.domain.service.message_publisher import MessagePublisher
from src.shared.database.domain.manager.transaction_manager import TransactionManager

@dataclass
class ServiceContainer:
    __services: Dict[str, Any] = field(default_factory=dict)
    __metadata: Metadata = None

    
    def __load_config(self, service: str) -> dict:
        yaml_path = None
        split = service.split('.')
        
        if 'command_handler' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/application/command_handlers.yaml'])
        if 'query_handler' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/application/query_handlers.yaml'])
        if 'repository' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/domain/model/repositories.yaml'])
        if 'manager' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/domain/manager/managers.yaml'])
        if 'service' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/domain/service/services.yaml'])
        if 'query_model' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/domain/query_model/queries.yaml'])
        if 'connection' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/domain/connection/connections.yaml'])
            
        if yaml_path is None:
            raise FileNotFoundError(f'YAML file not found for module: {service}')
        
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        
        if 'services' not in config:
            raise KeyError(f'The \'services\' key not found in YAML file: {yaml_path}')
        if service not in config['services']:
            raise KeyError(f'Service "{service}" not found in YAML file: {yaml_path}')
        
        return config['services'][service]
    
    
    def __get_class(self, reference_class: str) -> type:
        class_name = reference_class.rsplit('.', 1)[-1]

        module = import_module(reference_class)
        class_name_cammel_case = ''.join(word.capitalize() for word in class_name.split('_'))
        return getattr(module, class_name_cammel_case)
  
    
    def get(self, service: str) -> Any:
        if service in self.__services:
            return self.__services[service]
        
        service_config = self.__load_config(service)
        
        arguments = []
            
        for argument in service_config.get('arguments', []):
            if  argument.startswith('@'):
                arguments.append(self.get(argument[1:]))
            if  argument.startswith('%'):
                arguments.append(os.getenv(argument[1:]))
        
        self.__services[service] = self.__get_class(service_config['class'])(*arguments)

        return self.__services[service]
    
    @property
    def transaction_manager(self) ->  Union[TransactionManager, None]:
        return self.__services.get('src.shared.database.domain.manager.transaction_manager', None)
    
    @property
    def message_publisher(self) ->  Union[MessagePublisher, None]:
        return self.__services.get('src.shared.cqrs.domain.service.message_publisher', None)
    
    @property
    def metadata(self) -> Metadata:
        if self.__metadata:
            return Metadata(
                message_id = str(uuid.uuid4()),
                causation_id = self.__metadata.message_id,
                correlation_id = self.__metadata.correlation_id
            )
            
        return Metadata(
            message_id = str(uuid.uuid4()),
            causation_id = str(uuid.uuid4()),
            correlation_id = str(uuid.uuid4())
        )
        
    def initialize_metadata(self, metadata: Metadata) -> None:
        self.__metadata = metadata