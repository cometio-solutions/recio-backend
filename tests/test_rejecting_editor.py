"""Testing rejecting editor request"""
import json
import requests


def test_rejecting_editor_request():
    """
    Mustn't have emails 'reject_ed@test.agh.edu.pl' and 'reject_test@admin.agh.edu.pl'
    in database or test will fail.
    :return:
    """
    url_user = 'http://127.0.0.1:5000/user'
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_user_editor = 'http://127.0.0.1:5000/user/editorRequests'

    data = {'name': 'proper_name', 'email': 'reject_ed@test.agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    assert requests.post(url_user, json=data).status_code == 200

    data = {'name': 'admin', 'email': 'reject_test@admin.agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    assert requests.post(url_user, json=data).status_code == 200

    data = {'email': 'reject_test@admin.agh.edu.pl', 'password': '12345'}
    response = requests.post(url_user_auth, json=data)
    admin_login = json.loads(response.content.decode('utf-8'))

    data = {'email': 'reject_ed@test.agh.edu.pl', 'name': 'proper_name', 'approval': 'bad'}
    assert requests.post(
        url_user_editor,
        json=data,
        headers={'token': admin_login['token']}
    ).status_code == 409

    data = {'email': 'reject_ed@test.agh.edu.pl', 'name': 'proper_name', 'approval': 'reject'}
    assert requests.post(
        url_user_editor,
        json=data,
        headers={'token': admin_login['token']}
    ).status_code == 200

    response = requests.get(
        url_user_editor,
        headers={'token': admin_login['token']}
    )
    data = json.loads(response.content.decode('utf-8'))
    assert len(data) == 0
