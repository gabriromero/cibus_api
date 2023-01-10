from marshmallow import Schema, fields, validate


# Meal Schema
class MealSchema(Schema):
    id = fields.Int(dump_only=True)
    name     = fields.Str(required=True, validate=[validate.Length(min=2, max=80)])
    description  = fields.Str(required=True, validate=[validate.Length(min=2, max=256)])
    price = fields.Float(required=True, validate=[validate.Range(min=0.01, max=1000)])
    restaurant_id = fields.Int(required=True)

class MealUpdateSchema(Schema):
    name     = fields.Str(validate=[validate.Length(min=2, max=80)])
    description  = fields.Str(validate=[validate.Length(min=2, max=256)])
    price = fields.Float(validate=[validate.Range(min=0.01, max=1000)])


# Restaurant Schema
class RestaurantSchema(Schema):
    id = fields.Int(dump_only=True)
    name     = fields.Str(required=True, validate=[validate.Length(min=4, max=50)])
    address  = fields.Str(required=True, validate=[validate.Length(min=2, max=100)])

class RestaurantUpdateSchema(Schema):
    name     = fields.Str(validate=[validate.Length(min=4, max=50)])
    address  = fields.Str(validate=[validate.Length(min=2, max=100)])


# User schema
class LoginUserSchema(Schema):
    mail = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    mail = fields.Str(required=True, validate=[validate.Length(min=4, max=50)])
    password = fields.Str(required=True, load_only=True, validate=[validate.Length(min=6, max=50)])
    name     = fields.Str(required=True, validate=[validate.Length(min=2, max=50)])
    last_name= fields.Str(required=True, validate=[validate.Length(min=2, max=50)])
