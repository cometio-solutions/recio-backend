"""Testing getting points sum"""
import json
import subprocess
import os
import requests


def test_getting_points_sum():
    """
    Test getting points sum.
    :return:
    """
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_points_sum = 'http://127.0.0.1:5000/points'
    url_file_import = 'http://127.0.0.1:5000/file'
    generator_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../generator')

    # generating file
    return_code = subprocess.call('python3 generator.py 2 5', shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, cwd=generator_folder_path)
    assert return_code == 0

    # logging as a editor
    data = {'email': 'editor@agh.edu.pl', 'password': 'editor'}
    response = requests.post(url_user_auth, json=data)
    editor_login = json.loads(response.content.decode('utf-8'))

    # xlsx file
    files = {'data': ('data.xlsx', open(generator_folder_path + '/data.xlsx', 'rb'))}
    assert requests.post(url_file_import, files=files, headers={'token': editor_login['token']}).status_code == 200

    # get points sum
    response = requests.get(url_points_sum + '/1', headers={'token': editor_login['token']})
    assert response.status_code == 200

    # test data in response
    data = json.loads(response.content.decode('utf-8'))
    assert len(data) > 0
    assert isinstance(data, list)
    for d in data:
        assert isinstance(d, dict)
        assert isinstance(d['points'], int)
        assert isinstance(d['numberOfStudents'], int)

    # test bad recruitment id
    assert requests.get(url_points_sum + '/-1', headers={'token': editor_login['token']}).status_code == 404
