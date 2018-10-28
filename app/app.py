from flask import Flask
from resources.auth import auth_api
from config import config
from objects import db, api
from flask_cors import CORS
from models.user import UserModel
from sqlalchemy import func
import os
from time import sleep


def create_app() -> Flask:
    """
    An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :return: The initialized flask app
    """

    app: Flask = Flask("cryptic")

    app.config.update(**config)

    with app.app_context():
        if config["CROSS_ORIGIN"]:
            CORS(app)

        register_namespaces()

        sleep(1)

        register_extensions(app)
 
        setup_database()

        if config["DEBUG"]:
            setup_development_environment()

    return app


def register_extensions(app: Flask) -> None:
    """
    Registers flask extensions, such as the sqlalchemy.
    """

    db.init_app(app)
    api.init_app(app)


def register_namespaces() -> None:
    """
    This function registers all flask resources.
    """

    api.add_namespace(auth_api)


def setup_database() -> None:
    """
    Sets the database up.
    """

    while True:
        try:
            db.create_all()
            break
        except Exception as e:
            sleep(2)


def setup_development_environment() -> None:
    """
    Setup the development environment
    """

    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":  # Prevent from running twice
        if db.session.query(func.count(UserModel.uuid)).first()[0] == 0:
            UserModel.create("dev", "test", "@")


if __name__ == '__main__':
    app: Flask = create_app()
    app.run()
