import glob
from typing import Optional
from importlib import import_module
from src.shared.cqrs.domain.event.domain_event import DomainEvent

class DomainEventHydrator:
    
    @staticmethod
    def execute(routing_key: str, body: dict) -> Optional[DomainEvent]:
        pattern = 'src/*/*/domain/event/*.py'
        for file_path in glob.glob(pattern):
            with open(file_path, 'r') as file:
                if routing_key not in file.read():
                    continue
                
                reference_class = file_path.replace('/', '.').replace('\\', '.').replace('.py', '')
                class_name = reference_class.rsplit('.', 1)[-1]
                module = import_module(reference_class)

                class_name_cammel_case = ''.join(word.capitalize() for word in class_name.split('_'))
                return getattr(module, class_name_cammel_case)(*body.values())

        return None