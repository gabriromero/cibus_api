from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError

from db import db
from models import RestaurantModel, UserModel
from schemas import RestaurantSchema, RestaurantUpdateSchema

blp = Blueprint("Restaurants", __name__, description="Operations on restaurants")

@blp.route("/restaurant")
class Restaurant(MethodView):
    @blp.response(200, RestaurantSchema(many=True))
    def get(self):
        return RestaurantModel.query.all()

    @blp.arguments(RestaurantSchema)
    @blp.response(200, RestaurantSchema)
    def post(self, restaurant_data):

        if UserModel.query.get(restaurant_data["user_id"]) is None:
            abort(400,message="User does not exist")

        restaurant = RestaurantModel(
            name = restaurant_data["name"],
            address = restaurant_data["address"],
            user_id = restaurant_data["user_id"]
        )

        try:
            db.session.add(restaurant)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A restaurant with that name already exists")
        
        return restaurant, 201

@blp.route("/restaurant/<string:restaurant_id>")
class RestaurantCrud(MethodView):
    @blp.response(200, RestaurantSchema)
    def get(self,restaurant_id):
        store = RestaurantModel.query.get_or_404(restaurant_id)
        return store

    @blp.arguments(RestaurantUpdateSchema)
    @blp.response(200, RestaurantSchema)
    def put(self,restaurant_data, restaurant_id):
        restaurant = RestaurantModel.query.get_or_404(restaurant_id)
        
        if("name" in restaurant_data):
            restaurant.name = restaurant_data["name"]
        
        if("address" in restaurant_data):
            restaurant.address = restaurant_data["address"]

        db.session.add(restaurant)
        db.session.commit()

        return restaurant,200

    def delete(self,restaurant_id):
        restaurant = RestaurantModel.query.get_or_404(restaurant_id)

        db.session.delete(restaurant)
        db.session.commit()

        return {"message" : f"Restaurant with name '{restaurant.name}' deleted"}