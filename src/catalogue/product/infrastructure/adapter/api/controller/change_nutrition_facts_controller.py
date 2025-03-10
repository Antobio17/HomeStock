import traceback
from flask import request, jsonify
from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.utils.infrastructure.domain.service.check_param import CheckParam
from src.catalogue.product.application.command.change_nutrition_facts_command import ChangeNutritionFactsCommand
from src.catalogue.product.domain.exception.change_nutrition_facts_exception import ChangeNutritionFactsException
from src.authentication.oauth.infrastructure.domain.decorator.authorization_required_decorator import auth_required

@dataclass
class ChangeNutritionFactsController:
    __command_bus: CommandBus = field(default_factory=lambda: CommandBus())
    
    @auth_required
    def __invoke__(self, product_id: str):
        try:
            calories = CheckParam.get_float_request_param(request, 'calories')
            carbohydrates = CheckParam.get_float_request_param(request, 'carbohydrates')
            proteins = CheckParam.get_float_request_param(request, 'proteins')
            fats = CheckParam.get_float_request_param(request, 'fats')
            sugar = CheckParam.get_float_request_param(request, 'sugar')
            
            command = ChangeNutritionFactsCommand(
                product_id,
                calories,
                carbohydrates,
                proteins,
                fats,
                sugar
            )      
            self.__command_bus.handle(command)
        
            return '', 202
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
        except ChangeNutritionFactsException as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 400,
                            'title': 'An error occurred before changing nutrition facts.',
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
                            'title': 'An error occurred while changing nutrition facts.',
                            'details': str(e),
                            'trace': traceback.format_exc()
                        }
                    ]
                }, 500