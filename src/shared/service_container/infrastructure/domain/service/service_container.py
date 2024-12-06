import os
import yaml
from typing import Any, Dict
from sqlalchemy.orm import Session
from importlib import import_module
from dataclasses import dataclass, field
from src.shared.sqlalchemy.infrastructure.domain.model.writer_database_session import WriterDatabaseSession
from src.shared.sqlalchemy.infrastructure.domain.model.reader_database_session import ReaderDatabaseSession

@dataclass
class ServiceContainer:
    services: Dict[str, Any] = field(default_factory=dict)
    __writer_session = None
    __reader_session = None
    
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
            
        for argument in service_config.get('arguments', []):
            if not argument.startswith('@'):
                continue
            if argument == '@sqlalchemy_writer_session':
                arguments.append(self.get_writer_session())
                continue
            if argument == '@sqlalchemy_reader_session':
                arguments.append(self.get_reader_session())
                continue
            
            arguments.append(self.get(argument[1:]))
        
        self.services[service] =  self.__get_class(service_config['class'])(*arguments)
        
        return self.services[service]


    def get_writer_session(self) -> Session:
        if self.__writer_session is None:
            self.__writer_session = WriterDatabaseSession(os.getenv('DATABASE_WRITER_URL')).session
            
        return self.__writer_session
    
    
    def get_reader_session(self) -> Session:
        if self.__reader_session is None:
            self.__reader_session = WriterDatabaseSession(os.getenv('DATABASE_WRITER_URL')).session
            
        return self.__reader_session