from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError

from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from models import MealModel, RestaurantModel
from schemas import MealSchema, MealUpdateSchema

blp = Blueprint("Meals", __name__, description="Operations on meals")

@blp.route("/private/meals")
class PrivateMeals(MethodView):
    @blp.response(200, MealSchema(many=True))
    def get(self):
        return MealModel.query.all()

@blp.route("/restaurants/<string:restaurant_id>/meals")
class Meal(MethodView):
    @jwt_required()
    @blp.response(200)
    @blp.response(200, MealSchema(many=True))
    def get(self,restaurant_id):

        restaurant = RestaurantModel.query.get(restaurant_id)

        if restaurant is None:
            abort(400,message="Restaurant does not exist")

        if restaurant.user_id is not get_jwt_identity():
            abort(401)

        meals = restaurant.meals

        return meals

    @jwt_required()
    @blp.arguments(MealSchema)
    @blp.response(200, MealSchema)
    def post(self, meal_data, restaurant_id):

        restaurant = RestaurantModel.query.get(restaurant_id)

        if restaurant is None:
            abort(400,message="Restaurant does not exist")

        if restaurant.user_id is not get_jwt_identity():
            abort(401)

        meal = MealModel(
            name = meal_data["name"],
            description = meal_data["description"],
            price = meal_data["price"],
            restaurant_id = restaurant_id
        )

        db.session.add(meal)
        db.session.commit()
        
        return meal, 201


@blp.route("/restaurants/<string:restaurant_id>/meals/<string:meal_id>")
class MealCrud(MethodView):
    @jwt_required()
    @blp.arguments(MealUpdateSchema)
    @blp.response(200, MealSchema)
    def put(self, meal_data, restaurant_id, meal_id):
        restaurant = RestaurantModel.query.get(restaurant_id)

        if restaurant is None:
            abort(400,message="Restaurant does not exist")

        if restaurant.user_id is not get_jwt_identity():
            abort(401)

        meal = MealModel.query.get(meal_id)
        
        if("name" in meal_data):
            meal.name = meal_data["name"]
        
        if("description" in meal_data):
            meal.description = meal_data["description"]

        if("price" in meal_data):
            meal.price = meal_data["price"]

        db.session.add(meal)
        db.session.commit()

        return meal,200
    
    @jwt_required()
    def delete(self, restaurant_id, meal_id):
        restaurant = RestaurantModel.query.get(restaurant_id)

        if restaurant is None:
            abort(400,message="Restaurant does not exist")

        if restaurant.user_id is not get_jwt_identity():
            abort(401)
            
        meal = MealModel.query.get_or_404(meal_id)

        db.session.delete(meal)
        db.session.commit()

        return {"message" : f"Meal with name '{meal.name}' deleted"}

@blp.route("/meals/<string:meal_id>")
class MealCrud(MethodView):
    @blp.arguments(MealUpdateSchema)
    @blp.response(200, MealSchema)
    def put(self,meal_data, meal_id):
        meal = MealModel.query.get_or_404(meal_id)
        
        if("name" in meal_data):
            meal.name = meal_data["name"]
        
        if("description" in meal_data):
            meal.description = meal_data["description"]

        if("price" in meal_data):
            meal.price = meal_data["price"]

        db.session.add(meal)
        db.session.commit()

        return meal,200

    def delete(self,meal_id):
        meal = MealModel.query.get_or_404(meal_id)

        db.session.delete(meal)
        db.session.commit()

        return {"message" : f"Meal with name '{meal.name}' deleted"}

