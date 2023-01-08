from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from sqlalchemy.exc import IntegrityError
from blocklist import BLOCKLIST

from db import db
from models import UserModel
from schemas import UserSchema, LoginUserSchema

blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        user = UserModel(
            mail = user_data["mail"],
            password = pbkdf2_sha256.hash(user_data["password"]),
            name = user_data["name"],
            last_name = user_data["last_name"]
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A User with that username already exists")
        
        return user, 201

@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.mail == user_data["mail"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token" : access_token}
        
        abort(401, message="Invalid credentials")

@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message" : "Successfully logged out."}
        


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.response(201, UserSchema)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except IntegrityError:
            abort(400,message="First remove associated restaurants")

        return {"message" : "User deleted"}, 200


    