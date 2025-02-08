from typing import Union

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