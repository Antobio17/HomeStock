import os
import glob
import yaml
from flask.cli import FlaskGroup
from src.oauth import init_oauth
from flask import Flask, Blueprint
from importlib import import_module

def __get_class(reference_class: str) -> type:
    class_name = reference_class.rsplit('.', 1)[-1]
    
    module = import_module(reference_class)
    class_name_camel_case = ''.join(word.capitalize() for word in class_name.split('_'))
    return getattr(module, class_name_camel_case)

def __load_config(module: str) -> dict:
    split = module.split('.')
    yaml_path = '/'.join(split[:3] + ['infrastructure/adapter/api/routing.yaml'])
    
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    
    if 'endpoints' not in config:
        raise KeyError(f'The \'endpoints\' key not found in YAML file: {yaml_path}')
    if module not in config['endpoints']:
        raise KeyError(f'Module "{module}" not found in YAML file: {yaml_path}')
    
    return config['endpoints'][module]


def create_app():
    flask_app = Flask(__name__, instance_relative_config = True)
    flask_app.secret_key = os.getenv('SECRET_KEY')
    init_oauth(flask_app)
    
    pattern = 'src/*/*/infrastructure/adapter/api/controller/*.py'
    for filepath in glob.glob(pattern):
        module_name = filepath.replace('/', '.').replace('\\', '.').replace('.py', '')
        controller = __get_class(module_name)
        config = __load_config(module_name)
        
        main = Blueprint(config['name'], module_name)
        main.add_url_rule(config['path'], view_func = controller().__invoke__, methods = config['methods'])
        flask_app.register_blueprint(main)

    return flask_app

app = create_app()
app.run(host='0.0.0.0', port=80)

cli = FlaskGroup(app=app)
if __name__ == '__main__':
    cli()