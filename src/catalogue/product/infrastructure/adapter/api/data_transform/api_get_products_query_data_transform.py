from src.shared.cqrs.application.query.dto.query_result import QueryResult

class ApiGetProductsQueryDataTransform:
    
    @staticmethod
    def execute(result: QueryResult) -> dict:
        output = {
            'meta': {
                'aggregate': 'product',
                'pagination': {
                    'page': result.page,
                    'page_size': result.page_size,
                    'total': result.total
                }
            },
            'data': []
        }

        for item in result.result:
            output['data'].append({
                'id': item.id,
                'name': item.name,
                'calories': item.calories,
                'carbohydrates': item.carbohydrates,
                'proteins': item.proteins,
                'fats': item.fats,
                'sugar': item.sugar,
                'is_enabled': item.is_enabled
            })
            
        return output