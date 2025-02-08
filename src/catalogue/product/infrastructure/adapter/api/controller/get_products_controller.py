from dataclasses import dataclass, field
from flask import request, jsonify, Response # type: ignore
from src.shared.cqrs.application.query.query_bus import QueryBus
from src.shared.utils.infrastructure.domain.service.check_param import CheckParam
from src.catalogue.product.application.query.get_products_query import GetProductsQuery
from src.authentication.oauth.infrastructure.domain.decorator.authorization_required_decorator import auth_required
from src.catalogue.product.infrastructure.adapter.api.data_transform.api_get_products_query_data_transform import ApiGetProductsQueryDataTransform

@dataclass
class GetProductsController:
    __query_bus: QueryBus = field(default_factory=lambda: QueryBus())
    
    @auth_required
    def __invoke__(self):
        filters = CheckParam.get_filters_query(request)

        try:
            CheckParam.numeric_filter('price', filters, required = False)
            CheckParam.numeric_filter('calories', filters, required = False)
            CheckParam.numeric_filter('carbohydrates' ,filters, required = False)
            CheckParam.numeric_filter('proteins', filters, required = False)
            CheckParam.numeric_filter('fats' ,filters, required = False)
            CheckParam.numeric_filter('sugar' ,filters, required = False)
            
            result = self.__query_bus.handle(GetProductsQuery(
                name = filters.get('name', None),
                price = filters.get('price', None),
                calories = filters.get('calories', None),
                carbohydrates = filters.get('carbohydrates', None),
                proteins = filters.get('proteins', None),
                fats = filters.get('fats', None),
                sugar = filters.get('sugar', None),
                is_enabled = bool(filters.get('is_enabled', True)),
                page = filters.get('page', 1),
                page_size = filters.get('page_size', 10)                                     
            ))
        except ValueError as e:
            return Response(str(e), status = 400)
        except Exception as e:
            return Response(str(e), status = 500)
            
        return jsonify(
            ApiGetProductsQueryDataTransform().execute(result)    
        ), 200
    