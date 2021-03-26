import json
import requests


URL_USER = 'http://127.0.0.1:5000/user'
URL_USER_AUTH = 'http://127.0.0.1:5000/user/auth'
URL_USER_EDITOR = 'http://127.0.0.1:5000/user/editorRequests'


def test_valid_registration_input():
    data = {'name': 'proper_name', 'email': 'proper@agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 200

    data = {'name': 'proper_name', 'email': 'student@student.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 200

    data = {'name': 'proper_name', 'email': 'proper@agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 409

    data = {'name': '1', 'email': 'proper@agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 400

    data = {'name': '123', 'email': 'proper@gh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 400

    data = {'name': '123', 'email': 'proper@agh.edu.pl',
            'password': '45', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 400

    data = {'name': 'proper_name ', 'email': 'proper@agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(URL_USER, data=data).status_code == 400


def test_login():
    data = {'name': 'proper_name', 'email': 'login@agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    requests.post(URL_USER, data=data)
    login_data = {'email': 'login@agh.edu.pl', 'password': '12345'}
    assert requests.post(URL_USER_AUTH, data=login_data).status_code == 200

    login_data = {'email': 'login2@agh.edu.pl', 'password': '12345'}
    assert requests.post(URL_USER_AUTH, data=login_data).status_code == 400


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

    r = requests.get(
        URL_USER_EDITOR,
        cookies={'email': 'admin@admin.agh.edu.pl'}
    )
    assert r.status_code == 200
    data = json.loads(r.content.decode('utf-8'))
    assert len(data) == 1
    assert data[0]['name'] == 'proper_name'
    assert data[0]['user_email'] == 'register@agh.edu.pl'
