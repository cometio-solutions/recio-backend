import json
import requests


def test_login_role():
    """
    Mustn't have emails 'login_role@test.agh.edu.pl' and 'admin_test@admin.agh.edu.pl'
    in database or test will fail.
    :return: None
    """
    url_user = 'http://127.0.0.1:5000/user'
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_user_editor = 'http://127.0.0.1:5000/user/editorRequests'

    data = {'name': 'proper_name', 'email': 'login_role@test.agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    assert requests.post(url_user, data=data).status_code == 200

    login_data = {'email': 'login_role@test.agh.edu.pl', 'password': '12345'}
    response = requests.post(url_user_auth, data=login_data)
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert data['role'] == 'user'

    data = {'name': 'proper_name', 'email': 'login_role@test.agh.edu.pl'}
    response = requests.post(url_user_editor, data=data)
    assert response.status_code == 200

    response = requests.post(url_user_auth, data=login_data)
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert data['role'] == 'editor'

    data = {'name': 'admin_test', 'email': 'admin_test@admin.agh.edu.pl',
            'password': 'admin_test', 'editorRequest': False}
    assert requests.post(url_user, data=data).status_code == 200

    login_data = {'email': 'admin_test@admin.agh.edu.pl', 'password': 'admin_test'}
    response = requests.post(url_user_auth, data=login_data)
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert data['role'] == 'admin'
