import traceback
from flask import request, jsonify
from dataclasses import dataclass, field
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.utils.infrastructure.domain.service.check_param import CheckParam
from src.purchase.ticket.application.command.dto.submit_ticket_item import SubmitTicketItem
from src.purchase.ticket.application.command.submit_ticket_command import SubmitTicketCommand
from src.purchase.ticket.domain.exception.submit_ticket_exception import SubmitTicketException
from src.authentication.oauth.infrastructure.domain.decorator.authorization_required_decorator import auth_required

@dataclass
class SubmitTicketController:
    __command_bus: CommandBus = field(default_factory=lambda: CommandBus())
    
    @auth_required
    def __invoke__(self):
        try:
            supermarket = CheckParam.get_request_param(request, 'supermarket')
            reference = CheckParam.get_request_param(request, 'reference')
            subtotal = CheckParam.get_float_request_param(request, 'subtotal')
            discount_amount = CheckParam.get_float_request_param(request, 'discount_amount')
            taxes = CheckParam.get_dict_request_param(request, 'taxes')
            tax_amount = CheckParam.get_float_request_param(request, 'tax_amount')
            total = CheckParam.get_float_request_param(request, 'total')
            purchased_at = CheckParam.get_datetime_request_param(request, 'purchased_at')
            items = self.__get_items(request)
            
            command = SubmitTicketCommand(
                supermarket, 
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
        except SubmitTicketException as e:
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 400,
                            'title': 'An error occurred before submit ticket.',
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
                            'title': 'An error occurred while submitting ticket.',
                            'details': str(e),
                            'trace': traceback.format_exc()
                        }
                    ]
                }
            ), 500  
            
            
    def __get_items(self, request):
        items = []
        for item in CheckParam.get_list_request_param(request, 'items'):
            if not isinstance(item, dict):
                raise ValueError('Items should be a list of dictionaries.')
            
            items.append(
                SubmitTicketItem(
                    item.get('description', ''),
                    float(item.get('quantity', 0)),
                    float(item.get('amount', 0)),
                )
            )
        return items
             
