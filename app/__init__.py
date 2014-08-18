from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Database config
    config = os.path.join(app.root_path, 'config.cfg')
    app.config.from_pyfile(config)

    db.init_app(app)

    # Add the api
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app

