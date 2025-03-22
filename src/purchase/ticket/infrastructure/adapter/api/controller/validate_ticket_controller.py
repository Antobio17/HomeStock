import traceback
from flask import request, jsonify
from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.utils.infrastructure.domain.service.check_param import CheckParam
from src.purchase.ticket.application.command.dto.validate_ticket_item import ValidateTicketItem
from src.purchase.ticket.application.command.validate_ticket_command import ValidateTicketCommand
from src.purchase.ticket.domain.exception.validate_ticket_exception import ValidateTicketException
from src.authentication.oauth.infrastructure.domain.decorator.authorization_required_decorator import auth_required

@dataclass
class ValidateTicketController:
    __command_bus: CommandBus = field(default_factory=lambda: CommandBus())
    
    @auth_required
    def __invoke__(self, ticket_id: str):
        try:
            reference = CheckParam.get_request_param(request, 'reference')
            subtotal = CheckParam.get_float_request_param(request, 'subtotal')
            discount_amount = CheckParam.get_float_request_param(request, 'discount_amount')
            taxes = CheckParam.get_dict_request_param(request, 'taxes')
            tax_amount = CheckParam.get_float_request_param(request, 'tax_amount')
            total = CheckParam.get_float_request_param(request, 'total')
            purchased_at = CheckParam.get_datetime_request_param(request, 'purchased_at')
            items = self.__get_items(request)
            
            command = ValidateTicketCommand(
                ticket_id,
                reference,
                subtotal,
                discount_amount,
                taxes,
                tax_amount,
                total,
                purchased_at,
                items
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
        except ValidateTicketException as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 400,
                            'title': 'An error occurred before validate ticket.',
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
                            'title': 'An error occurred while validating ticket.',
                            'details': str(e),
                            'trace': traceback.format_exc()
                        }
                    ]
                }
            ), 500  
            
            
    def __get_items(self, request) -> list[ValidateTicketItem]:
        items = []
        for item in CheckParam.get_list_request_param(request, 'items'):
            if not isinstance(item, dict):
                raise ValueError('Items should be a list of dictionaries.')
            
            items.append(
                ValidateTicketItem(
                    item.get('description', ''),
                    float(item.get('quantity', 0)),
                    float(item.get('amount', 0)),
                    item.get('product_id', None),
                    item.get('format_id', None)
                )
            )
        return items
             
