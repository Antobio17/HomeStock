from flask import request, Response # type: ignore

class GetProductsController:
    def __init__(self):
        pass
    
    def __invoke__(self):
        return Response(response='OK', status = 201)