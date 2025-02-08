class Utils:
    
    @staticmethod
    def mapping_operations(operation: str) -> str:
        if operation == 'eq':
            return '='
        if operation == 'gt':
            return '>'
        if operation == 'lt':
            return '<'
        if operation == 'gte':
            return '>='
        if operation == 'lte':
            return '<='
        if operation == 'ne':
            return '!='
        
        raise ValueError(f'Mapping operation for {operation} not found')
    
    @staticmethod
    def add_condition_query(where_clause: str, field_name: str, conditions: dict) -> str:
        for operation in conditions.keys():
            where_clause += f' {field_name} {Utils.mapping_operations(operation)} {conditions[operation]} AND'
        return where_clause 