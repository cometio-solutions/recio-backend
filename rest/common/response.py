"""This module has functions for responses in routes"""
import json
from flask import Response


def create_response(data, status, origin=None, headers=None):
    """
    Create and return flask Response object with given attributes.
    Should be used especially if headers are needed to make less code.

    :param data: information you want to send in json format
    :param status: response status (e.g. 200, 400, 401)
    :param origin: set Access-Control-Allow-Origin header in response, needed for CORS
    :param headers: set Access-Control-Allow-Headers header in response, needed for CORS
    :return: flask Response object
    """
    response = Response(response=json.dumps(data), status=status, mimetype='application/json')

    if origin is not None:
        response.headers.add('Access-Control-Allow-Origin', origin)

    if headers is not None:
        response.headers.add('Access-Control-Allow-Headers', headers)

    return response
