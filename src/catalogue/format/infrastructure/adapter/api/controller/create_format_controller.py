import traceback
from flask import request, jsonify
from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.utils.infrastructure.domain.service.check_param import CheckParam
from src.catalogue.format.application.command.create_format_command import CreateFormatCommand
from src.catalogue.format.domain.exception.create_format_exception import CreateFormatException
from src.authentication.oauth.infrastructure.domain.decorator.authorization_required_decorator import auth_required

@dataclass
class CreateFormatController:
    __command_bus: CommandBus = field(default_factory=lambda: CommandBus())
    
    @auth_required
    def __invoke__(self):
        try:
            product_id = CheckParam.get_request_param(request, 'product_id')
            name = CheckParam.get_request_param(request, 'name')
            
            command = CreateFormatCommand(product_id, name)     
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
        except CreateFormatException as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 400,
                            'title': 'An error occurred before creating format.',
                            'details': e.message
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
                            'title': 'An error occurred while creating format.',
                            'details': str(e),
                            'trace': traceback.format_exc()
                        }
                    ]
                }
            ), 500  
             
