import glob
import yaml
from src.shared.message_broker.infrastructure.domain.connection.rabbitmq.rabbitmq_connection import RabbitmqConnection

class RabbitmqSetupFabric:
    
    def __init__(self):
        self.rabbitmq_connection = RabbitmqConnection()
    
    def execute(self):
        self.__declare_exchanges()
        self.__declare_queues()
            
    def __declare_exchanges(self):
        yaml_paths = glob.glob('/app/src/*/shared/infrastructure/adapter/messaging/rabbitmq.yaml')

        exchanges = []
        for yaml_path in yaml_paths:
            with open(yaml_path, 'r') as file:
                config = yaml.safe_load(file)
                exchanges += config['rabbitmq']['exchange']
        
        for exchange in exchanges:     
            self.rabbitmq_connection.exchange_declare(
                exchange = exchange['name'],
                exchange_type = exchange['type'],
                durable = exchange.get('durable', True),
                auto_delete = exchange.get('auto_delete', False)
            )
            
    def __declare_queues(self):
        yaml_paths = glob.glob('/app/src/*/shared/infrastructure/adapter/messaging/rabbitmq.yaml')

        queues = []
        for yaml_path in yaml_paths:
            with open(yaml_path, 'r') as file:
                config = yaml.safe_load(file)
                queues += config['rabbitmq']['queue']
        
        for queue in queues:
            self.rabbitmq_connection.queue_declare(
                queue = queue['name'],
                durable = queue.get('durable', True),
                auto_delete = queue.get('auto_delete', False)
            )
            
            for binding in queue.get('bindings', []):
                self.rabbitmq_connection.queue_bind(
                    queue = queue['name'],
                    exchange = binding['exchange'],
                    routing_key = binding['routing_key']
                )
        

    
if __name__ == "__main__":
    RabbitmqSetupFabric().execute()