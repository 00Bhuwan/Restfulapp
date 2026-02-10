import os

from flask import Flask
from flask_migrate import Migrate
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

from db import db


def create_app(db_url=None):
    app = Flask(__name__)

    print(">>> create_app CALLED <<<")
    print(">>> db_url:", db_url)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores RESTAPI"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"

    # --- DATABASE CONFIG ---
    uri = db_url or os.getenv("DATABASE_URL", "sqlite:///datanew.db")

    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    if "@db:" in uri:
        uri = uri.replace("@db:", "@localhost:")

    print(">>> FINAL DB URI:", uri)

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # -----------------------

    db.init_app(app)
    Migrate(app, db)

    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    return app
