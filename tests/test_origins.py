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
    generator_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../generator')

    # generating file
    return_code = subprocess.call('python3 generator.py 1', shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, cwd=generator_folder_path)
    assert return_code == 0

    data = {'email': 'file_import@admin.agh.edu.pl', 'password': '12345'}
    response = requests.post(url_user_auth, json=data)
    admin_login = json.loads(response.content.decode('utf-8'))

    response = requests.get(url_origins, headers={'token': admin_login['token']})
    assert response.status_code == 200

    data = json.loads(response.content.decode('utf-8'))
    assert len(data.keys()) == 17
    assert isinstance(data['Inne'], int)
