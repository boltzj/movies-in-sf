from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    # Read config from object
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    # Add the api
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
