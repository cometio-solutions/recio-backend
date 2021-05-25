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
    url_recruitment = 'http://127.0.0.1:5000/recruitment/'

    data = {'email': 'editor@agh.edu.pl', 'password': 'editor'}
    response = requests.post(url_user_auth, json=data)
    editor_login = json.loads(response.content.decode('utf-8'))

    # generating file
    generator_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../generator')
    return_code = subprocess.call('python3 generator.py 1 2', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=generator_folder_path)
    assert return_code == 0

    # importing file
    files = {'data':('candidates.csv', open(generator_folder_path + '/candidates.csv', 'rb'))}
    assert requests.post(url_file_import, files=files, headers={'token': editor_login['token']}
    ).status_code == 200

    # not auth
    assert requests.get(
        url_recruitment + '1'
    ).status_code == 401

    # recruitment not found
    assert requests.get(
        url_recruitment + '9999',
        headers={'token': editor_login['token']}
    ).status_code == 404

    # testing fetching specific recruitment with id=1
    assert requests.get(
        url_recruitment + '1',
        headers={'token': editor_login['token']}
    ).status_code == 200

    # testing fetching next recruitment cycle
    response = requests.get(
        url_recruitment + '1/next',
        headers={'token': editor_login['token']}
    )
    assert response.status_code == 200
    data = json.loads(response.content.decode('utf-8'))

    assert requests.get(
        url_recruitment + str(data['id']) + '/next',
        headers={'token': editor_login['token']}
    ).status_code == 404

    # testing fetching previous recruitment cycle
    assert requests.get(
        url_recruitment + str(data['id']) + '/previous',
        headers={'token': editor_login['token']}
    ).status_code == 200

    assert requests.get(
        url_recruitment + '1/previous',
        headers={'token': editor_login['token']}
    ).status_code == 404