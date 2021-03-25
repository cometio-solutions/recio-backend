import requests


url_user = "http://127.0.0.1:5000/user"
url_user_auth = "http://127.0.0.1:5000/user/auth"
url_user_editor = "http://127.0.0.1:5000/user/editorRequests"


def test_valid_registration_input():
    data = {"name": "proper_name", "email": "proper@agh.edu.pl", "password": "12345", "editorRequest": False}
    assert requests.post(url_user, data=data).status_code == 200

    data = {"name": "proper_name", "email": "proper@agh.edu.pl", "password": "12345", "editorRequest": False}
    assert requests.post(url_user, data=data).status_code == 409

    data = {"name": "1", "email": "proper@agh.edu.pl", "password": "12345", "editorRequest": False}
    assert requests.post(url_user, data=data).status_code == 400

    data = {"name": "123", "email": "proper@gh.edu.pl", "password": "12345", "editorRequest": False}
    assert requests.post(url_user, data=data).status_code == 400

    data = {"name": "123", "email": "proper@agh.edu.pl", "password": "45", "editorRequest": False}
    assert requests.post(url_user, data=data).status_code == 400

    data = {"name": "proper_name ", "email": "proper@agh.edu.pl", "password": "12345", "editorRequest": False}
    assert requests.post(url_user, data=data).status_code == 400


def test_login():
    data = {"name": "proper_name", "email": "login@agh.edu.pl", "password": "12345", "editorRequest": False}
    requests.post(url_user, data=data)
    login_data = {"email": "login@agh.edu.pl", "password": "12345"}
    assert requests.post(url_user_auth, data=login_data).status_code == 200

    login_data = {"email": "login2@agh.edu.pl", "password": "12345"}
    assert requests.post(url_user_auth, data=login_data).status_code == 400


def test_admin_editor_request():
    data = {"name": "proper_name", "email": "register@agh.edu.pl", "password": "12345", "editorRequest": False}
    requests.post(url_user, data=data)
    assert requests.get(url_user_editor).status_code == 401
    assert requests.get(url_user_editor, cookies={"email": "register@agh.edu.pl"}).status_code == 403
    assert requests.get(url_user_editor, cookies={"email": "non_existed_register@agh.edu.pl"}).status_code == 403
