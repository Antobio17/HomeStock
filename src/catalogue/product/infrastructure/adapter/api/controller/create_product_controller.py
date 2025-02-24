import traceback
from flask import request, jsonify # type: ignore
from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.utils.infrastructure.domain.service.check_param import CheckParam
from src.catalogue.product.application.command.create_product_command import CreateProductCommand
from src.catalogue.product.domain.exception.create_product_exception import CreateProductException
from src.authentication.oauth.infrastructure.domain.decorator.authorization_required_decorator import auth_required

@dataclass
class CreateProductController:
    __command_bus: CommandBus = field(default_factory=lambda: CommandBus())
    
    @auth_required
    def __invoke__(self):
        try:
            name = CheckParam.get_form_param(request, 'name')
            
            command = CreateProductCommand(name)     
            self.__command_bus.handle(command) 
            
            return '', 201 
        except ValueError as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 400,
                            'title': 'An error occurred while checking form params.',
                            'details': str(e)
                        }
                    ]
                }    
            ), 400
        except CreateProductException as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 400,
                            'title': 'An error occurred before creating product.',
                            'details': str(e)
                        }
                    ]
                }    
            ), 400
        except Exception as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 500,
                            'title': 'An error occurred while creating product.',
                            'details': str(e),
                            'trace': traceback.format_exc()
                        }
                    ]
                }
            ), 500  
             
