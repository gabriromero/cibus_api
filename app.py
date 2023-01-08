import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate

from dotenv import load_dotenv

from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST

from db import db

from resources.user import blp as UserBlueprint
from resources.restaurant import blp as RestaurantBlueprint
from resources.meal import blp as MealBlueprint

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Cibus REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
    jwt =  JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {"description" : "Token has been revoked"}
        ),401,

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(RestaurantBlueprint)
    api.register_blueprint(MealBlueprint)

    return app