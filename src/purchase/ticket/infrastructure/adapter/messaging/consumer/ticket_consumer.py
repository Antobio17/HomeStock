from src.shared.message_broker.infrastructure.adapter.messaging.consumer.rabbitmq_consumer import RabbitmqConsumer

class TicketConsumer(RabbitmqConsumer):
    pass
    
if __name__ == '__main__':
    TicketConsumer('purchase', 'ticket').execute()