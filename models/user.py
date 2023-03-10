from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name     = db.Column(db.String(80), nullable=False)
    last_name= db.Column(db.String(80), nullable=False)

    restaurants = db.relationship("RestaurantModel", back_populates="user", lazy="dynamic")
