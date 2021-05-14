"""Testing getting origins"""
import json
import subprocess
import os
import requests


def test_getting_origins():
    """
    Test getting candidate origins.
    :return:
    """
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_origins = 'http://127.0.0.1:5000/origins'
    url_file_import = 'http://127.0.0.1:5000/file'
    generator_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../generator')

    # generating file
    return_code = subprocess.call('python3 generator.py 1 2', shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, cwd=generator_folder_path)
    assert return_code == 0

    data = {'email': 'editor@agh.edu.pl', 'password': 'editor'}
    response = requests.post(url_user_auth, json=data)
    editor_login = json.loads(response.content.decode('utf-8'))

    # xlsx file
    files = {'data': ('data.xlsx', open(generator_folder_path + '/data.xlsx', 'rb'))}
    assert requests.post(url_file_import, files=files, headers={'token': editor_login['token']}
     ).status_code == 200

    # test good request
    response = requests.get(url_origins + '/1', headers={'token': editor_login['token']})
    assert response.status_code == 200

    data = json.loads(response.content.decode('utf-8'))
    assert len(data.keys()) == 17
    assert isinstance(data['Inne'], int)

    # test bad recruitment id request
    assert requests.get(url_origins + '/-1', headers={'token': editor_login['token']}).status_code == 404
