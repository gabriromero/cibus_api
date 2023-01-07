from db import db

class MealModel(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), unique=False, nullable=False)

    restaurant = db.relationship("RestaurantModel", back_populates="meals")