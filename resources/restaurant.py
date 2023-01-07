from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import IntegrityError

from db import db
from models import RestaurantModel
from schemas import RestaurantSchema

blp = Blueprint("Restaurants", __name__, description="Operations on restaurants")

@blp.route("/restaurant")
class Register(MethodView):
    @blp.arguments(RestaurantSchema)
    @blp.response(200, RestaurantSchema)
    def post(self, restaurant_data):
        restaurant = RestaurantModel(
            name = restaurant_data["name"],
            address = restaurant_data["address"],
        )

        try:
            db.session.add(restaurant)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A restaurant with that name already exists")
        
        return restaurant, 201