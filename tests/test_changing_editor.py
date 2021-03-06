"""Testing changing editor status, but only with 'approve': 'accept'"""
import json
import requests


def test_changing_editor_status():
    """
    Mustn't have emails 'editor@test.agh.edu.pl' and 'admin_test3@admin.agh.edu.pl'
    in database or test will fail.
    :return: None
    """
    url_user = 'http://127.0.0.1:5000/user'
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_user_editor = 'http://127.0.0.1:5000/user/editorRequests'

    data = {'name': 'proper_name', 'email': 'editor@test.agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    assert requests.post(url_user, json=data).status_code == 200

    data = {'name': 'proper_name', 'email': 'editor@test.agh.edu.pl'}
    assert requests.post(url_user_editor, json=data).status_code == 401

    data = {'email': 'editor@test.agh.edu.pl', 'password': '12345'}
    response = requests.post(url_user_auth, json=data)
    non_admin_login = json.loads(response.content.decode('utf-8'))

    data['approval'] = 'accept'
    assert requests.post(
        url_user_editor,
        data=data,
        headers={'token': non_admin_login['token']}
    ).status_code == 403

    data = {'name': 'admin_test', 'email': 'admin_test3@admin.agh.edu.pl',
            'password': 'admin_test', 'editorRequest': False}
    assert requests.post(url_user, json=data).status_code == 200

    data = {'email': 'admin_test3@admin.agh.edu.pl', 'password': 'admin_test'}
    response = requests.post(url_user_auth, json=data)
    admin_login = json.loads(response.content.decode('utf-8'))

    data = {'name': 'proper_name', 'email': 'editor@test.agh.edu.pl', 'approval': 'accept'}
    response = requests.post(
        url_user_editor,
        json=data,
        headers={'token': admin_login['token']}
    )
    assert response.status_code == 200

    response = requests.get(
        url_user_editor,
        headers={'token': admin_login['token']}
    )
    data = json.loads(response.content.decode('utf-8'))
    assert len(data) == 0

    data = {'name': 'proper_name', 'email': 'invalid@test.agh.edu.pl', 'approval': 'accept'}
    response = requests.post(
        url_user_editor,
        json=data,
        headers={'token': admin_login['token']}
    )
    assert response.status_code == 409
