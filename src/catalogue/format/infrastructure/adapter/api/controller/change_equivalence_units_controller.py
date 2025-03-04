import traceback
from flask import request, jsonify
from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.utils.infrastructure.domain.service.check_param import CheckParam
from src.authentication.oauth.infrastructure.domain.decorator.authorization_required_decorator import auth_required
from src.catalogue.format.application.command.change_equivalence_units_command import ChangeEquivalenceUnitsCommand
from src.catalogue.format.domain.exception.change_equivalence_units_exception import ChangeEquivalenceUnitsException

@dataclass
class ChangeEquivalenceUnitsController:
    __command_bus: CommandBus = field(default_factory=lambda: CommandBus())
    
    @auth_required
    def __invoke__(self, format_id: str):
        try:
            recipe_unit = CheckParam.get_form_param(request, 'recipe_unit')
            storage_unit = CheckParam.get_form_param(request, 'storage_unit')
            storage_unit_equivalence = CheckParam.get_float_form_param(request, 'storage_unit_equivalence')
            purchase_unit = CheckParam.get_form_param(request, 'purchase_unit')
            purchase_unit_equivalence = CheckParam.get_float_form_param(request, 'purchase_unit_equivalence')
            purchase_price = CheckParam.get_float_form_param(request, 'purchase_price')
            
            command = ChangeEquivalenceUnitsCommand(
                format_id,
                recipe_unit,
                storage_unit,
                storage_unit_equivalence,
                purchase_unit,
                purchase_unit_equivalence,
                purchase_price
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
        except ChangeEquivalenceUnitsException as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 400,
                            'title': 'An error occurred before changing equivalence units.',
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
                            'title': 'An error occurred while changing equivalence units.',
                            'details': str(e),
                            'trace': traceback.format_exc()
                        }
                    ]
                }, 500