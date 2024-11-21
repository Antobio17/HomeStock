import yaml
from typing import Any, Dict
from importlib import import_module

class ServiceContainer:

    def __init__(self):
        self.services: Dict[str, Any] = {}
        
        
    def __load_config(self, module_path: str) -> dict:
        if 'command_handler' in module_path:
            split = module_path.split('.')
            yaml_path = '/'.join(split[:3] + ['infrastructure/application/command_handlers.yaml'])
            
        if 'repository' in module_path:
            split = module_path.split('.')
            yaml_path = '/'.join(split[:3] + ['infrastructure/domain/model/repositories.yaml'])
            
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)
    
    
    def __get_class(self, module_path: str) -> type:
        module_name, class_name = module_path.rsplit('.', 1)

        module = import_module(module_name + '.' + class_name)
        class_name_cammel_case = ''.join(word.capitalize() for word in class_name.split('_'))
        return getattr(module, class_name_cammel_case)
        
        
    
    def get(self, service: str) -> Any:
        if service in self.services:
            return self.services[service]
        
        config = self.__load_config(service)
        service_config = config['services'][service]
        
        args = []
        if 'arguments' in service_config:
            for arg in service_config['arguments']:
                if isinstance(arg, str) and arg.startswith('@'):
                    args.append(self.get(arg[1:]))
                else:
                    args.append(arg)
        
        class_imported = self.__get_class(service_config['class'])
        self.services[service] = class_imported(*args)
        
        return self.services[service]
