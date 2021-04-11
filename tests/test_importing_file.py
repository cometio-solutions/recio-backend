"""Testing importing file"""
import json
import subprocess
import os
import requests


def test_rejecting_editor_request():
    """
    Test for file import
    :return:
    """
    url_user = 'http://127.0.0.1:5000/user'
    url_user_auth = 'http://127.0.0.1:5000/user/auth'
    url_user_editor = 'http://127.0.0.1:5000/user/editorRequests'
    url_file_import = 'http://127.0.0.1:5000/file'
    generator_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../generator')

    # generating file
    return_code = subprocess.call('python3 generator.py 1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=generator_folder_path)
    assert return_code == 0


    data = {'name': 'proper_name', 'email': 'file_import@editor.agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    assert requests.post(url_user, json=data).status_code == 200

    data = {'name': 'admin', 'email': 'file_import@admin.agh.edu.pl',
            'password': '12345', 'editorRequest': True}
    assert requests.post(url_user, json=data).status_code == 200

    data = {'email': 'file_import@admin.agh.edu.pl', 'password': '12345'}
    response = requests.post(url_user_auth, json=data)
    admin_login = json.loads(response.content.decode('utf-8'))

    data = {'email': 'file_import@editor.agh.edu.pl', 'name': 'proper_name', 'approval': 'accept'}
    assert requests.post(
        url_user_editor,
        json=data,
        headers={'token': admin_login['token']}
    ).status_code == 200

    data = {'email': 'file_import@editor.agh.edu.pl', 'password': '12345'}
    response = requests.post(url_user_auth, json=data)
    editor_login = json.loads(response.content.decode('utf-8'))

    # not editor
    assert requests.post(url_file_import, headers={'token': admin_login['token']}
    ).status_code == 403

    # no file
    assert requests.post(url_file_import, headers={'token': editor_login['token']}
    ).status_code == 400

    # bad file
    files = {'data':('generator.py', open(generator_folder_path + '/generator.py', 'rb'))}
    assert requests.post(url_file_import, headers={'token': editor_login['token']}
    ).status_code == 400

    # xlsx file
    files = {'data':('data.xlsx', open(generator_folder_path + '/data.xlsx', 'rb'))}
    assert requests.post(url_file_import, files=files, headers={'token': editor_login['token']}
    ).status_code == 200

    # csv file
    files = {'data':('candidates.csv', open(generator_folder_path + '/candidates.csv', 'rb'))}
    assert requests.post(url_file_import, files=files, headers={'token': editor_login['token']}
    ).status_code == 200
