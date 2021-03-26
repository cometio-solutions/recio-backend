import json
import requests


def test_admin_editor_request():
    """
    Mustn't have emails 'register_req@test.agh.edu.pl' and 'admin_test2@admin.agh.edu.pl'
    in database or test will fail.
    :return: None
    """
    url_user = 'http://127.0.0.1:5000/user'
    url_user_editor = 'http://127.0.0.1:5000/user/editorRequests'

    data = {'name': 'proper_name', 'email': 'register_req@test.agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    assert requests.post(url_user, data=data).status_code == 200

    assert requests.get(url_user_editor).status_code == 401

    assert requests.get(
        url_user_editor,
        cookies={'email': 'register_req@test.agh.edu.pl'}
    ).status_code == 403

    assert requests.get(
        url_user_editor,
        cookies={'email': 'non_existed_register@agh.edu.pl'}
    ).status_code == 403

    data = {'name': 'admin_test', 'email': 'admin_test2@admin.agh.edu.pl',
            'password': 'admin_test', 'editorRequest': True}
    assert requests.post(url_user, data=data).status_code == 200

    response = requests.get(
        url_user_editor,
        cookies={'email': 'admin_test2@admin.agh.edu.pl'}
    )
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))
    assert len(data) == 1
    assert data[0]['name'] == 'proper_name'
    assert data[0]['user_email'] == 'register_req@test.agh.edu.pl'
