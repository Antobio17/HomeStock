from flask import Blueprint, request, Response # type: ignore

class GetProductsController:
    def __init__(self):
        self.main = Blueprint('get_products', __name__)
        self.main.add_url_rule('/v1/products', view_func = self.__invoke__, methods = ['GET'])    
    
    def __invoke__(self):
        return Response(response='OK', status = 201)