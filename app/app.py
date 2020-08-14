from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown

from app.db import db
from app.models.user import User
from .router import routes



def create_app(config):
    """Instantiates Flask app

    This creates a Flask application instance using
    application factory pattern with the a config and
    return an instance of the app with some configurations

    :param config: Flask configuration from file
    :return: app
    :rtype: object
    """

    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config)

    return app


def register_extensions(app):
    """Register all Extensions
    This registers all the add-ons of the app,
    to be instantiated with the instance of the flask app
    Add your extensions to this functions e.g Mail

    :param app: Flask app instance
    :return: None
    :rtype: NoneType
    """

    db.db.init_app(app)
    routes(app)
    login = LoginManager(app)
    bootstrap = Bootstrap(app)
    Markdown(app)


    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
