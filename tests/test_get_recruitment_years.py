"""Testing getting recruitment years"""
import json
import subprocess
import os
import requests


def test_getting_recruitment_years():
    """
    Test for getting recruitment years
    :return:
    """
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_years = 'http://127.0.0.1:5000/years'
    url_file_import = 'http://127.0.0.1:5000/file'
    generator_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../generator')

    # generating file
    return_code = subprocess.call('python3 generator.py 1', shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, cwd=generator_folder_path)
    assert return_code == 0

    data = {'email': 'editor@agh.edu.pl', 'password': 'editor'}
    response = requests.post(url_user_auth, json=data)
    editor_login = json.loads(response.content.decode('utf-8'))

    files = {'data': ('candidates.csv', open(generator_folder_path + '/candidates.csv', 'rb'))}
    assert requests.post(url_file_import, files=files, headers={'token': editor_login['token']}
    ).status_code == 200

    response = requests.get(url_years, headers={'token': editor_login['token']})
    assert response.status_code == 200
    years = json.loads(response.content.decode('utf-8'))
    assert isinstance(years, list)
    assert len(years) > 0
