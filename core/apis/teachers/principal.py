from flask import request, Blueprint,jsonify
from core import db
from core.models import Teacher ,User
from .schema import TeacherSchema, UserSchema
from core.apis.responses import APIResponse
from core.apis import decorators 

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)
principal_users_resources = Blueprint('principal_users_resources', __name__)



@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of Teachers"""
    principals_teachers = Teacher.get_teachers()
    teachers_dump = TeacherSchema().dump(principals_teachers, many=True)
    return APIResponse.respond(data=teachers_dump)


@principal_users_resources.route('/users', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def list_users(p,incoming_payload):
    """Returns list of Users, can be filtered by id or email"""
    
    user_id = incoming_payload.get('id')
    user_email = incoming_payload.get('email')
    print(user_id, user_email)
    users=[]
    if user_id:
        users.append(User.get_by_id(user_id))
    if user_email:
        users.append(User.get_by_email(user_email))
    if not user_id and not user_email:
        users = User.query.all()


    # Return the users as a response
    users_dump = UserSchema().dump(users, many=True) 
    return APIResponse.respond(data=users_dump)