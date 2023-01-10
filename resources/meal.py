from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError

from db import db
from models import MealModel, RestaurantModel
from schemas import MealSchema, MealUpdateSchema

blp = Blueprint("Meals", __name__, description="Operations on meals")

@blp.route("/meals")
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


@blp.route("/meals/<string:meal_id>")
class MealCrud(MethodView):
    @blp.response(200, MealSchema)
    def get(self,meal_id):
        meal = MealModel.query.get_or_404(meal_id)
        return meal

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

