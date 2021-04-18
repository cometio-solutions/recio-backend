"""This module contains endpoints connected to getting data used for filtering"""
from flask import Blueprint, request
from rest.common.response import create_response
from rest.common.token import handle_request_token


filter_url = Blueprint('filter', __name__)


@filter_url.before_request
def handle_options():
    """
    Handles OPTIONS method before recruitment endpoint
    :return: flask Response object with status 200 if the method is OPTIONS, else None
    """
    headers = 'content-type, token'

    if request.method == 'OPTIONS':
        return create_response({}, 200, '*', headers)

    return None


@filter_url.route('/fields', methods=['GET', 'OPTIONS'])
def get_fields():
    """
    Gets all fields of study for filtering purposes
    :return: json list of fields of study
    """
    role, response = handle_request_token(request)

    if role is None:
        return response

    fields_list = []

    try:
        with open('generator/field_of_studies', 'r', encoding='utf-8') as fields:
            for field in fields:
                fields_list.append(field.strip('\n'))
    except IOError:
        return create_response({'error': 'Nie udało się wczytać listy kierunków.'}, 500, '*')

    return create_response(fields_list, 200, '*')
