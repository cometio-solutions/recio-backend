"""Testing calculating point limit"""
import json
import subprocess
import os
import requests


def test_calculate_point_limit_request():
    """
    Test for calculating point limit, requires editor@agh.edu.pl account to exists
    :return:
    """
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_point_limit = 'http://127.0.0.1:5000/point-limit'
    url_file_import = 'http://127.0.0.1:5000/file'
    url_recruitment = 'http://127.0.0.1:5000/recruitment'
    generator_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../generator')

    # generating file
    return_code = subprocess.call('python3 generator.py 5', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=generator_folder_path)
    assert return_code == 0

    data = {'email': 'editor@agh.edu.pl', 'password': 'editor'}
    response = requests.post(url_user_auth, json=data)
    editor_login = json.loads(response.content.decode('utf-8'))

    # importing file
    files = {'data':('data.xlsx', open(generator_folder_path + '/data.xlsx', 'rb'))}
    assert requests.post(url_file_import, files=files, headers={'token': editor_login['token']}
    ).status_code == 200

    # no auth
    assert requests.post(url_point_limit).status_code == 401

    # calculating point limits
    assert requests.post(url_point_limit, headers={'token': editor_login['token']}).status_code == 200

    # testing if it worked
    response = requests.get(url_recruitment,headers={'token': editor_login['token']})
    assert response.status_code == 200
    data = json.loads(response.content)
    for recruitment in data['data']:
        if not recruitment['is_active']:
            assert recruitment['point_limit'] is not None
