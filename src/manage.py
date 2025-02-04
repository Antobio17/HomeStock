import glob
from flask import Flask # type: ignore
from flask.cli import FlaskGroup # type: ignore
from src.oauth import init_oauth
from importlib import import_module


def __get_class(reference_class: str) -> type:
    class_name = reference_class.rsplit('.', 1)[-1]
    
    module = import_module(reference_class)
    class_name_cammel_case = ''.join(word.capitalize() for word in class_name.split('_'))
    return getattr(module, class_name_cammel_case)


def create_app():
    app = Flask(__name__, instance_relative_config = True)
    app.secret_key = 'your secret key'
    init_oauth(app)
    
    pattern = 'src/*/*/infrastructure/adapter/api/controller/*.py'
    for filepath in glob.glob(pattern):
        module_name = filepath.replace('/', '.').replace('\\', '.').replace('.py', '')
        controller = __get_class(module_name)
        app.register_blueprint(controller().main)

    return app

app = create_app()
app.run(host='0.0.0.0', port=80)

cli = FlaskGroup(app) 
if __name__ == "__main__":
    cli()