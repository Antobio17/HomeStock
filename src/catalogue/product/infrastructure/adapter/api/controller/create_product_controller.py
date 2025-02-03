from flask import Blueprint, request, Response # type: ignore
from src.shared.cqrs.application.command.command_bus import CommandBus
from src.shared.utils.infrastructure.domain.service.check_param import CheckParam
from src.catalogue.product.application.command.create_product_command import CreateProductCommand

class CreateProductController:
    def __init__(self):
        self.main = Blueprint('create_product', __name__)
        self.main.add_url_rule('/v1/products', view_func = self.__invoke__, methods = ['POST'])
        self.command_bus = CommandBus()
    
    
    def __invoke__(self):
        try:
            name = CheckParam.get_form_param(request, 'name')
            price = CheckParam.get_float_form_param(request, 'price')
            calories = CheckParam.get_int_form_param(request, 'calories')
            carbohydrates = CheckParam.get_int_form_param(request, 'carbohydrates')
            proteins = CheckParam.get_int_form_param(request, 'proteins')
            fats = CheckParam.get_int_form_param(request, 'fats')
            sugar = CheckParam.get_int_form_param(request, 'sugar')
            is_enabled = CheckParam.get_boolean_form_param(request, 'is_enabled', required = False)
            
            command = CreateProductCommand(
                name,
                price,
                calories,
                carbohydrates,
                proteins,
                fats,
                sugar,
                is_enabled
            )      
            self.command_bus.handle(command)  
        except ValueError as e:
            return Response(str(e), status = 400)
        except Exception as e:
            return Response(str(e), status = 500)
        
        return Response(status = 201)