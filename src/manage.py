import glob
import importlib
from flask import Flask
from flask.cli import FlaskGroup

def create_app():
    app = Flask(__name__, instance_relative_config = True)

    pattern = 'src/*/*/infrastructure/adapter/api/controller/*.py'
    for filepath in glob.glob(pattern):
        module_name = filepath.replace('/', '.').replace('\\', '.').replace('.py', '')
        module = importlib.import_module(module_name)
        app.register_blueprint(module.main)

    return app

app = create_app()
app.run(host='0.0.0.0', port=80)

cli = FlaskGroup(app)
if __name__ == "__main__":
    cli()