from marshmallow import Schema, fields, validate

# User schema

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    mail = fields.Str(required=True, validate=[validate.Length(min=4, max=50)])
    password = fields.Str(required=True, load_only=True, validate=[validate.Length(min=6, max=50)])
    name     = fields.Str(required=True, validate=[validate.Length(min=2, max=50)])
    last_name= fields.Str(required=True, validate=[validate.Length(min=2, max=50)])

class LoginUserSchema(Schema):
    mail = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)