import yaml
from typing import Any, Dict
from importlib import import_module
from dataclasses import dataclass, field
from src.shared.sqlalchemy.infrastructure.domain.model.database_session import DatabaseSession

@dataclass
class ServiceContainer:
    services: Dict[str, Any] = field(default_factory=dict)
        
    def __load_config(self, service: str) -> dict:
        yaml_path = None
        split = service.split('.')
        
        if 'command_handler' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/application/command_handlers.yaml'])
            
        if 'query_handler' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/application/query_handlers.yaml'])
            
        if 'repository' in service:
            yaml_path = '/'.join(split[:3] + ['infrastructure/domain/model/repositories.yaml'])
            
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
        if service in self.services:
            return self.services[service]
        
        service_config = self.__load_config(service)
        
        arguments = []
        
        if 'repository' in service:
            arguments.append(DatabaseSession().writer_session)
            
        for argument in service_config.get('arguments', []):
            if not argument.startswith('@'):
                continue
            
            arguments.append(self.get(argument[1:]))
        
        self.services[service] =  self.__get_class(service_config['class'])(*arguments)
        
        return self.services[service]
