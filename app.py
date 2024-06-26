from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_smorest import Api
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager
from resource.item import blp as ItemBlueprint
from resource.store import blp as StoreBlueprint
from resource.user import blp as UserBlueprint
from resource.tag import blp as TagBlueprint
from schemas.db import db_data
from blocklist import BLOCKLIST
from dotenv import load_dotenv
import models
import os
import redis
from rq import Queue


def create_app(db_url= None):
    app = Flask(__name__)

    load_dotenv()

    connection= redis.from_url(
        os.getenv('REDIS_URL')
    )
    
    app.queue = Queue("email", connection= connection)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "STORES API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///database.sqlite")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    db_data.init_app(app)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "isongrichard234@gmail.com"
    app.config['MAIL_PASSWORD'] = "Imisioluwa234."
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    
    migrate = Migrate(app, db_data)
    api = Api(app)


    app.config["JWT_SECRET_KEY"] = "Richard"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({
                "message" : "The token has expired.", "error" : "token_expired"
            }),
            401
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify(
                {
                    "message" : "Signature verification failed.", "error" : "invalid_token" 
                }
            ),
            401,
        )


    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token",
                    "error" : "authorization_required",
                }
            ),
            401
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description" : "The token is not fresh.",
                    "error" : "fresh_token_required"
                }
            ),
            401
        )
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description": "The token has been revoked.", "error" : "token_revoked"}
            ),
            401
        )
    
    #JWT configuration ends 




    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TagBlueprint)

    return app








    

