from marshmallow import Schema, fields, validate

# User schema
class LoginUserSchema(Schema):
    mail = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class RestaurantSchema(Schema):
    id = fields.Int(dump_only=True)
    name     = fields.Str(required=True, validate=[validate.Length(min=4, max=50)])
    address  = fields.Str(required=True, validate=[validate.Length(min=2, max=100)])
    user_id = fields.Int(required=True)

class RestaurantUpdateSchema(Schema):
    name     = fields.Str()
    address  = fields.Str()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    mail = fields.Str(required=True, validate=[validate.Length(min=4, max=50)])
    password = fields.Str(required=True, load_only=True, validate=[validate.Length(min=6, max=50)])
    name     = fields.Str(required=True, validate=[validate.Length(min=2, max=50)])
    last_name= fields.Str(required=True, validate=[validate.Length(min=2, max=50)])
