"""Recruitment endpoints tests"""
import json
import requests


def test_recruitment_data():
    """
    Tests gathering recruitment data
    """

    url_user = 'http://127.0.0.1:5000/user'
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_recruitment = 'http://127.0.0.1:5000/recruitment'

    data = {'name': 'recruitment_test', 'email': 'recruitment@test.agh.edu.pl',
            'password': '12345', 'editorRequest': True}

    assert requests.post(url_user, json=data).status_code == 200

    data = {'email': 'recruitment@test.agh.edu.pl', 'password': '12345'}
    response = requests.post(url_user_auth, json=data)
    non_admin_login = json.loads(response.content.decode('utf-8'))

    assert requests.get(
        url_recruitment,
        headers={'token': non_admin_login['token']}
    ).status_code == 200
