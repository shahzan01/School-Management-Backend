from flask import request, Blueprint,jsonify
from core import db
from core.models.teachers import Teacher
from .schema import TeacherSchema
from core.apis.responses import APIResponse
from core.apis import decorators 

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of Teachers"""
    try:
        principals_teachers = Teacher.get_teachers()
        teachers_dump = TeacherSchema().dump(principals_teachers, many=True)
        return APIResponse.respond(data=teachers_dump)
    except Exception as e:
        return APIResponse.respond(message=f"Error fetching teachers: {str(e)}", status_code=500)

