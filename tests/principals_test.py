from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]




def test_get_teachers(client, h_principal):
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for teacher in data:
        assert teacher['id'] is not None



def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'Assignment must be submitted before it can be graded.'


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B




def test_grade_assignment_without_auth(client):
    """
    failure case: Unauthorized user should not be able to grade an assignment
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        }
    )
    assert response.status_code == 401
    data = response.json
    assert data['error'] == 'FyleError'
    assert data["message"] == 'principal not found'


def test_list_users_by_id(client, h_principal):
    sample_user = {
            "email": "student2@fylebe.com",
            "id": 2,
            "username": "student2"}
    
    """Test listing users by id"""
    response = client.post('/principal/users', json={'id': sample_user['id']}, headers=h_principal)
    
    assert response.status_code == 200
    data = response.json
    assert len(data['data']) == 1
    assert data['data'][0]['username'] == sample_user["username"]  # ✅ Fixed
    assert data['data'][0]['email'] == sample_user["email"] 



def test_list_users_by_email(client, h_principal):
    sample_user = {
            "email": "student2@fylebe.com",
            "id": 2,
            "username": "student2"}
    
    """Test listing users by id"""
    response = client.post('/principal/users', json={'email': sample_user['email']} , headers=h_principal)
    
    assert response.status_code == 200
    data = response.json
    assert len(data['data']) == 1
    assert data['data'][0]['username'] == sample_user["username"]  # ✅ Fixed
    assert data['data'][0]['email'] == sample_user["email"] 


def test_list_all_users(client, h_principal):
    """Test listing all the users when no filter is applied"""
    response = client.post('/principal/users', json={} , headers=h_principal)
    
    assert response.status_code == 200
    data = response.json
    assert len(data['data']) >= 1
