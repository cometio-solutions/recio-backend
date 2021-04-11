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


@file_url.route('', methods=['POST', 'OPTIONS'])
def upload_file():
    """
    Endpoint for file import.
    :return: success status if file was imported correctly or error otherwise
    """
    if request.method == 'OPTIONS':
        headers = 'content-type, token'
        return create_response({}, 200, '*', headers)

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
        if not os.path.exists("files/"):
            os.makedirs("files/")
        file_path = os.path.join("files/", secure_filename(uploaded_file.filename))
        uploaded_file.save(file_path)
        data = parse_file(file_path)
        save_data(data)
        # removing file after save
        os.remove(file_path)
        response_data = {"message": "Zaimportowano plik."}
        response_status_code = 200
        # pylint: disable=broad-except
    except Exception as exception:
        print(exception, file=sys.stderr)
        response_data = {"error": "Nie udało się zaimportować pliku."}
        response_status_code = 400

    return create_response(response_data, response_status_code, '*')
