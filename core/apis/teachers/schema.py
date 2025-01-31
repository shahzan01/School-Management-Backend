from marshmallow import Schema, EXCLUDE, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.models import users 
from core.libs.helpers import GeneralObject
from core.models import Teacher ,User


class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE
        include_fk = True 

    id = auto_field(required=False, allow_none=True)
    user_id = auto_field() 
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
   



class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        unknown = EXCLUDE
        include_fk = True

    id = fields.Int(required=False, allow_none=True)
    username = fields.Str()
    email = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)