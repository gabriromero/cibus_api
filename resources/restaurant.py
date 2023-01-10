
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required, get_jwt_identity

from sqlalchemy.exc import IntegrityError

from db import db
from models import RestaurantModel, UserModel
from schemas import RestaurantSchema, RestaurantUpdateSchema

from decorators.admin import admin_required

        
blp = Blueprint("Restaurants", __name__, description="Operations on restaurants")

@blp.route("/restaurants")
class Restaurant(MethodView):
    @blp.response(200, RestaurantSchema(many=True))
    @jwt_required()
    @admin_required()
    def get(self):
        return RestaurantModel.query.filter_by(user_id=get_jwt_identity())

    @blp.arguments(RestaurantSchema)
    @blp.response(200, RestaurantSchema)
    @jwt_required()
    def post(self, restaurant_data):

        restaurant = RestaurantModel(
            name = restaurant_data["name"],
            address = restaurant_data["address"],
            user_id = get_jwt_identity()
        )

        try:
            db.session.add(restaurant)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A restaurant with that name already exists")
        
        return restaurant, 201

@blp.route("/restaurants/<string:restaurant_id>")
class RestaurantCrud(MethodView):
    @blp.response(200, RestaurantSchema)
    @jwt_required()
    def get(self,restaurant_id):
        restaurant = RestaurantModel.query.get_or_404(restaurant_id)

        if restaurant.user_id is not get_jwt_identity():
            abort(401)

        return restaurant

    @blp.arguments(RestaurantUpdateSchema)
    @blp.response(200, RestaurantSchema)
    @jwt_required()
    def put(self,restaurant_data, restaurant_id):
        restaurant = RestaurantModel.query.get_or_404(restaurant_id)

        if restaurant.user_id is not get_jwt_identity():
            abort(401)
        
        if("name" in restaurant_data):
            restaurant.name = restaurant_data["name"]
        
        if("address" in restaurant_data):
            restaurant.address = restaurant_data["address"]

        db.session.add(restaurant)
        db.session.commit()

        return restaurant,200

    @jwt_required()
    def delete(self,restaurant_id):
        restaurant = RestaurantModel.query.get_or_404(restaurant_id)

        if restaurant.user_id is not get_jwt_identity():
            abort(401)

        try:
            db.session.delete(restaurant)
            db.session.commit()
        except IntegrityError:
            abort(400,message="First remove associated meals")

        return {"message" : f"Restaurant with name '{restaurant.name}' deleted"}