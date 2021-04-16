"""Testing filter/fields GET"""
import requests
import json


def test_getting_fields_of_study():
    """
    Test getting fields of study, requires editor@agh.edu.pl account to exists.
    Changing file generator/field_of_studies will probably make this test fail.
    :return: None
    """
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_filter_fields = 'http://127.0.0.1:5000/filter/fields'

    data = {'email': 'editor@agh.edu.pl', 'password': 'editor'}
    response = requests.post(url_user_auth, json=data)
    editor_login = json.loads(response.content.decode('utf-8'))

    response = requests.get(url_filter_fields, headers={'token': editor_login['token']})
    assert response.status_code == 200
    data = json.loads(response.content)
    assert isinstance(data, list)
    assert len(data) > 0
    assert len(data) == 69
    assert data[68] == 'ZARZĄDZANIE I INŻYNIERIA PRODUKCJI'
