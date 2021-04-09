"""This module contains endpoints connected with file"""
import os
import sys
from flask import request, Blueprint
from werkzeug.utils import secure_filename
from rest.common.response import create_response
from rest.common.token import handle_request_token
from rest.common.parsing import parse_file, save_data


file_url = Blueprint('file', __name__)
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}


def check_file_name(filename):
    """
    Checks if uploaded file has proper name
    :param filename: Name of the uploaded file
    :return: True if filename is correct, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@file_url.before_request
def handle_options():
    """
    Handles OPTIONS method for all file routes.
    :return: flask Response object with status 200 if the method is OPTIONS, else None
    """
    headers = 'content-type, token'

    if request.method == 'OPTIONS':
        return create_response({}, 200, '*', headers)

    return None


@file_url.route('', methods=['POST', 'OPTIONS'])
def upload_file():
    """
    Either get (GET) editor requests or handle (POST) editor request, accept or reject.
    Requires 'email' field in cookies.
    if method GET and status 200 returns json:
        list of [
            'name': name
            'email': email
        ]
    :return: success status and json editor requests (if GET)
    """
    role, response = handle_request_token(request)

    if role is None:
        return response

    if role != 'editor':
        return create_response({"error": "Tylko edytor ma możliwość dodawania plików."}, 403, '*')

    if 'data' not in request.files:
        return create_response({"error": "Nie znaleziono pliku."}, 400, '*')
    uploaded_file = request.files['data']

    if not uploaded_file or not check_file_name(uploaded_file.filename):
        return create_response({"error": "Plik ma nieprawidłowe rozszerzenie."}, 400, '*')

    try:
        file_path = os.path.join("files/", secure_filename(uploaded_file.filename))
        uploaded_file.save(file_path)
        data = parse_file(file_path)
        save_data(data)
        # pylint: disable=broad-except
    except Exception as exception:
        print(exception, file=sys.stderr)
        return create_response({"error": "Nie udało się zaimportować pliku."}, 400, '*')

    return create_response({"message": "Zaimportowano plik."}, 200, '*')
