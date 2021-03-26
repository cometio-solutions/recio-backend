import json
import requests


URL_USER = 'http://127.0.0.1:5000/user'
URL_USER_AUTH = 'http://127.0.0.1:5000/user/auth'
URL_USER_EDITOR = 'http://127.0.0.1:5000/user/editorRequests'

"""
Before running these tests there cannot be users with these emails in database:
'proper@test.agh.edu.pl'
'proper@test.student.agh.edu.pl'
'login@agh.edu.pl'
'register@agh.edu.pl'
in database or it will fail.

'docker-compose up' must be run before so that requests go through.
"""


def test_valid_registration_input():
    data = {'name': 'proper_name', 'email': 'proper@test.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 200

    data = {'name': 'proper_name', 'email': 'proper@test.student.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 200

    data = {'name': 'proper_name', 'email': 'proper@test.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 409

    data = {'name': '1', 'email': 'proper@test.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 400

    data = {'name': '123', 'email': 'proper@test.gh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 400

    data = {'name': '123', 'email': 'proper@test.agh.edu.pl',
            'password': '45', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 400

    data = {'name': 'proper_name ', 'email': 'proper@test.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 400


def test_login():
    data = {'name': 'proper_name', 'email': 'login@agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    requests.post(URL_USER, data=data)
    login_data = {'email': 'login@agh.edu.pl', 'password': '12345'}
    assert requests.post(URL_USER_AUTH, data=login_data).status_code == 200

    login_data = {'email': 'login2@agh.edu.pl', 'password': '12345'}
    assert requests.post(URL_USER_AUTH, data=login_data).status_code == 400

    login_data = {'email': 'login@agh.edu.pl', 'password': '123435'}
    assert requests.post(URL_USER_AUTH, data=login_data).status_code == 400


def test_login_role():
    login_data = {'email': 'login@agh.edu.pl', 'password': '12345'}
    response = requests.post(URL_USER_AUTH, data=login_data)
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert data['role'] == 'user'

    data = {'name': 'proper_name', 'email': 'login@agh.edu.pl'}
    response = requests.post(URL_USER_EDITOR, data=data)
    assert response.status_code == 200

    response = requests.post(URL_USER_AUTH, data=login_data)
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert data['role'] == 'editor'

    login_data = {'email': 'admin@admin.agh.edu.pl', 'password': 'admin'}
    response = requests.post(URL_USER_AUTH, data=login_data)
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert data['role'] == 'admin'


def test_admin_editor_request():
    data = {'name': 'proper_name', 'email': 'register@agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    requests.post(URL_USER, data=data)

    assert requests.get(URL_USER_EDITOR).status_code == 401

    assert requests.get(
        URL_USER_EDITOR,
        cookies={'email': 'register@agh.edu.pl'}
    ).status_code == 403

    assert requests.get(
        URL_USER_EDITOR,
        cookies={'email': 'non_existed_register@agh.edu.pl'}
    ).status_code == 403

    response = requests.get(
        URL_USER_EDITOR,
        cookies={'email': 'admin@admin.agh.edu.pl'}
    )
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert len(data) == 1
    assert data[0]['name'] == 'proper_name'
    assert data[0]['user_email'] == 'register@agh.edu.pl'


def test_changing_editor_status():
    data = {'name': 'proper_name', 'email': 'register@agh.edu.pl'}
    response = requests.post(URL_USER_EDITOR, data=data)
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert data['is_editor']

    response = requests.get(
        URL_USER_EDITOR,
        cookies={'email': 'admin@admin.agh.edu.pl'}
    )
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert len(data) == 0

    data = {'name': 'proper_name', 'email': 'register@agh.edu.pl'}
    response = requests.post(URL_USER_EDITOR, data=data)
    assert response.status_code == 400
