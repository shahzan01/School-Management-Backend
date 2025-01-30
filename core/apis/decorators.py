import json
from flask import request
from core.libs import assertions
from functools import wraps

class AuthPrincipal:
    def __init__(self, user_id, student_id=None, teacher_id=None, principal_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.principal_id = principal_id


def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper

def verify_user_role(user_id, role_id, model, role_name):
    if role_id is not None:
        # Check if the role exists in the database
        role_instance = model.query.get(role_id)
        assertions.assert_found(role_instance, f'{role_name} not found')
        assertions.assert_valid(user_id == role_instance.user_id, f'User ID does not match the {role_name} ID')



def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')
        p_dict = json.loads(p_str)
        p = AuthPrincipal(
            user_id=p_dict['user_id'],
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )

        from core.models import Student, Teacher, Principal
        if p.student_id is not None:
            verify_user_role(p.user_id, p.student_id, Student, 'Student')

        if p.teacher_id is not None:
            verify_user_role(p.user_id, p.teacher_id, Teacher, 'Teacher')

        if p.principal_id is not None:
            verify_user_role(p.user_id, p.principal_id, Principal, 'Principal')



        if request.path.startswith('/student'):
            assertions.assert_true(p.student_id is not None, 'requester should be a student')
        elif request.path.startswith('/teacher'):
            assertions.assert_true(p.teacher_id is not None, 'requester should be a teacher')
        elif request.path.startswith('/principal'):
            assertions.assert_true(p.principal_id is not None, 'requester should be a principal')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper
