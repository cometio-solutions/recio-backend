"""Recruitment endpoints tests"""
import json
import subprocess
import os
import requests


def test_recruitment_data():
    """
    Tests gathering recruitment data for specific recruitment. Requires editor@agh.edu.pl account to exists
    """
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_file_import = 'http://127.0.0.1:5000/file'
    url_recruitment = 'http://127.0.0.1:5000/recruitment/1'

    data = {'email': 'editor@agh.edu.pl', 'password': 'editor'}
    response = requests.post(url_user_auth, json=data)
    editor_login = json.loads(response.content.decode('utf-8'))

    # generating file
    generator_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../generator')
    return_code = subprocess.call('python3 generator.py 1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=generator_folder_path)
    assert return_code == 0

    # importing file
    files = {'data':('candidates.csv', open(generator_folder_path + '/candidates.csv', 'rb'))}
    assert requests.post(url_file_import, files=files, headers={'token': editor_login['token']}
    ).status_code == 200

    # testing fetching specific recruitment with id=1
    assert requests.get(
        url_recruitment,
        headers={'token': editor_login['token']}
    ).status_code == 200
