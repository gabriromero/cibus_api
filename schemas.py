from marshmallow import Schema, fields

# User schema

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    mail = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    name     = fields.Str(required=True)
    last_name= fields.Str(required=True)

class LoginUserSchema(Schema):
    mail = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)