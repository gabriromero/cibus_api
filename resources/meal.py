from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError

from db import db
from models import MealModel, RestaurantModel
from schemas import MealSchema

blp = Blueprint("Meals", __name__, description="Operations on meals")

@blp.route("/meal")
class Meal(MethodView):
    @blp.response(200, MealSchema(many=True))
    def get(self):
        return MealModel.query.all()

    @blp.arguments(MealSchema)
    @blp.response(200, MealSchema)
    def post(self, meal_data):

        if RestaurantModel.query.get(meal_data["restaurant_id"]) is None:
            abort(400,message="Restaurant does not exist")

        meal = MealModel(
            name = meal_data["name"],
            description = meal_data["description"],
            price = meal_data["price"],
            restaurant_id = meal_data["restaurant_id"]
        )

        db.session.add(meal)
        db.session.commit()
        
        return meal, 201

"""
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

        return {"message" : f"Restaurant with id {restaurant.id} deleted"}

"""