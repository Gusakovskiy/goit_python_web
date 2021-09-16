import os

from flask import Flask
from . import db
from . import auth
from . import todo


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping()
    directory_path = os.getcwd()
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile(os.path.join(directory_path, 'config.py'), silent=True)  # DO not do this on prod
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(todo.todo_bp)
    app.add_url_rule('/', endpoint='index')

    return app

# export FLASK_APP=personal_app
# export FLASK_ENV=development
# runs on https://werkzeug.palletsprojects.com/en/2.0.x/
# flask run