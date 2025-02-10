from flask import request, jsonify # type: ignore
from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.utils.infrastructure.domain.service.check_param import CheckParam
from src.catalogue.product.application.command.update_product_command import UpdateProductCommand
from src.catalogue.product.domain.exception.update_product_exception import UpdateProductException
from src.authentication.oauth.infrastructure.domain.decorator.authorization_required_decorator import auth_required

@dataclass
class UpdateProductController:
    __command_bus: CommandBus = field(default_factory=lambda: CommandBus())
    
    @auth_required
    def __invoke__(self, id: str):
        try:
            name = CheckParam.get_form_param(request, 'name')
            price = CheckParam.get_float_form_param(request, 'price')
            calories = CheckParam.get_int_form_param(request, 'calories')
            carbohydrates = CheckParam.get_int_form_param(request, 'carbohydrates')
            proteins = CheckParam.get_int_form_param(request, 'proteins')
            fats = CheckParam.get_int_form_param(request, 'fats')
            sugar = CheckParam.get_int_form_param(request, 'sugar')
            
            command = UpdateProductCommand(
                id,
                name,
                price,
                calories,
                carbohydrates,
                proteins,
                fats,
                sugar
            )      
            self.__command_bus.handle(command)  
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
        except UpdateProductException as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 400,
                            'title': 'An error occurred before updating product.',
                            'details': str(e)
                        }
                    ]
                }    
            ), 400
        except Exception as e:
            return {
                    'errors': [
                        {
                            'status': 500,
                            'title': 'An error occurred while updating product.',
                            'details': str(e)
                        }
                    ]
                }, 500
        
        return '', 201
