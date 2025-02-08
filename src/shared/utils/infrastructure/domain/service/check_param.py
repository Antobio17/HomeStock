from typing import Union
from src.shared.utils.infrastructure.domain.service.utils import Utils

class CheckParam:
    
    @staticmethod
    def get_form_param(request, param_name: str, required: bool = True) -> Union[str, None]:
        value = request.form.get(param_name)
        if required and value is None:
            raise ValueError(f'Parameter {param_name} is required.')
        
        return value
    
    @staticmethod
    def get_numeric_form_param(request, param_name: str, required: bool = True) -> Union[str, None]:
        value = CheckParam.get_form_param(request, param_name, required)
        if not value.isnumeric():
            raise ValueError(f'Parameter {param_name} must be numeric.')
        
        return value
    
    @staticmethod
    def get_int_form_param(request, param_name: str, required: bool = True) -> Union[int, None]:
        value = CheckParam.get_numeric_form_param(request, param_name, required)
        return int(value)
    
    @staticmethod
    def get_float_form_param(request, param_name: str, required: bool = True) -> Union[float, None]:
        value = CheckParam.get_numeric_form_param(request, param_name, required)
        return float(value)
    
    @staticmethod
    def get_boolean_form_param(request, param_name: str, required: bool = True) -> Union[bool, None]:
        value = CheckParam.get_form_param(request, param_name, required)
        return value.lower() == 'true' or value == '1' if value is not None else None
    
    @staticmethod
    def get_filters_query(request) -> dict:
        filters = {}
        for key in request.args:
            if '[' not in key:
                filters[key] = request.args.get(key)
                continue
                
            param_name, operator = key.split('[')
            operator = operator.rstrip(']')
            if param_name not in filters:
                filters[param_name] = {}
            
            filters[param_name][operator] = request.args.get(key)
        
        return filters
    
    @staticmethod
    def numeric_filter(param_name: str, filter, required: bool = True) -> None:
        if filter[param_name] is None and required:
            raise ValueError(f'Param {param_name} is required.')
        
        if not isinstance(filter[param_name], dict):
            raise ValueError(f'Numeric filter format should be `param[operation]=value` for {param_name}.')
        
        for operation in filter[param_name].keys():
            Utils.mapping_operations(operation)
            if not isinstance(filter[param_name][operation], (int, float, complex)):
                raise ValueError(f'Values from {param_name} should be numeric.')
