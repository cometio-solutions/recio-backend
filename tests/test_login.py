import requests


def test_login():
    """
    Mustn't have emails 'login@test.agh.edu.pl' and 'login2@test.agh.edu.pl'
    in database or test will fail.
    :return: None
    """
    url_user = 'http://127.0.0.1:5000/user'
    url_user_auth = 'http://127.0.0.1:5000/user/auth'

    data = {'name': 'proper_name', 'email': 'login@test.agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    assert requests.post(url_user, json=data).status_code == 200

    login_data = {'email': 'login@test.agh.edu.pl', 'password': '12345'}
    assert requests.post(url_user_auth, json=login_data).status_code == 200

    login_data = {'email': 'login2@test.agh.edu.pl', 'password': '12345'}
    assert requests.post(url_user_auth, json=login_data).status_code == 400

    login_data = {'email': 'login@test.agh.edu.pl', 'password': '123435'}
    assert requests.post(url_user_auth, json=login_data).status_code == 400
