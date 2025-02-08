from flask import request, jsonify # type: ignore
from dataclasses import dataclass, field
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
            CheckParam.numeric_filter('price', filters, is_required = False)
            CheckParam.numeric_filter('calories', filters, is_required = False)
            CheckParam.numeric_filter('carbohydrates' ,filters, is_required = False)
            CheckParam.numeric_filter('proteins', filters, is_required = False)
            CheckParam.numeric_filter('fats' ,filters, is_required = False)
            CheckParam.numeric_filter('sugar' ,filters, is_required = False)
            
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
            return jsonify(
                {
                    'errors': [
                        {
                            'status': 400,
                            'title': 'An error occurred while checking filters.',
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
                            'title': 'An error occurred while retrieving products.',
                            'details': str(e)
                        }
                    ]
                }, 500
            
        return jsonify(
            ApiGetProductsQueryDataTransform().execute(result)    
        ), 200
    