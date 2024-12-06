from src.catalogue.product.application.command.create_product_command import CreateProductCommand
from src.shared.cqrs.application.command.command_bus import CommandBus

class CreateProductCommandCli:
    
    def __init__(self):
        self.command_bus = CommandBus()
    
    def execute(self) -> None:
        
        command = CreateProductCommand(
            'holaa2',
            1.0,
            1,
            1,
            1,
            1,
            1,
            True
        )
        self.command_bus.handle(command)
    
    
if __name__ == "__main__":
    CreateProductCommandCli().execute()