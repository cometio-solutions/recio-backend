"""This module has functions for token handling in routes"""
import logging

import jwt
from flask import current_app
from rest.common.response import create_response


def handle_request_token(request):
    """
    Handles authorization token in request. If there is an error in the token returns
    a pair (None, flask Response object) if there is no error returns pair (string, None),
    where string is user role ('user', 'editor', 'admin').
    So to check if error occurred compare first return value to None, if True -> error.
    :param request: incoming request that should contain 'token' field in header
    :return: pair (role, Response) where one value is None
    """
    logging.info("Trying to handle request")
    if 'token' not in request.headers:
        logging.warning("Token not provided")
        return None, create_response({'error': 'Musisz być zalogowany'}, 401, '*')

    try:
        token = jwt.decode(
            request.headers['token'],
            current_app.config['SECRET_KEY'],
            algorithms='HS256'
        )
    except jwt.ExpiredSignatureError:
        logging.warning("Session expired")
        return None, create_response({'error': 'Sesja wygasła, zaloguj się ponownie'}, 401, '*')
    except jwt.InvalidSignatureError:
        logging.warning("Bad token provided!")
        return None, create_response({'error': 'Nieprawidłowa sygnatura tokenu!'}, 401, '*')

    role = token['role']

    logging.info("Properly handled request")

    return role, None
