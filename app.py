from flask import Flask
from flask_smorest import Api
from resource.item import blp as ItemBlueprint
from resource.store import blp as StoreBlueprint
from db import db_data
import models
import os


def create_app(db_url= None):
    app = Flask(__name__)


    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "STORES API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/imisi-swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///database.sqlite")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    db_data.init_app(app)


    api = Api(app)

    
    with app.app_context():
        db_data.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app








    

