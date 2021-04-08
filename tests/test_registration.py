"""Testing registration POST"""
import requests


def test_valid_registration_input():
    """
    Mustn't have emails 'register@test.agh.edu.pl' and 'register@test.student.agh.edu.pl'
    in database or test will fail.
    :return: None
    """
    url = 'http://127.0.0.1:5000/user'

    data = {'name': 'Proper Name', 'email': 'register@test.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(url, json=data).status_code == 200

    data = {'name': 'Józef śniezynski', 'email': 'reg@test.student.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(url, json=data).status_code == 200

    data = {'name': 'Proper Name', 'email': 'register@test.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(url, json=data).status_code == 409

    data = {'name': '1', 'email': 'register@test.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(url, json=data).status_code == 400

    data = {'name': '123', 'email': 'register@test.gh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(url, json=data).status_code == 400

    data = {'name': '123', 'email': 'register@test.agh.edu.pl',
            'password': '45', 'editorRequest': False}
    assert requests.post(url, json=data).status_code == 400

    data = {'name': 'not!proper_name ', 'email': 'proper@test.agh.edu.pl',
            'password': '12345', 'editorRequest': False}
    assert requests.post(url, json=data).status_code == 400
