"""This module contains endpoints connected with users"""
from datetime import datetime, timedelta
import jwt
from flask import request, Blueprint, current_app
from rest.db import db
from rest.models.user import User
from rest.models.editor_request import EditorRequest
from rest.common.response import create_response
from rest.common.token import handle_request_token

user_url = Blueprint('user', __name__)


@user_url.before_request
def handle_options():
    """
    Handles OPTIONS method for all user routes.
    :return: flask Response object with status 200 if the method is OPTIONS, else None
    """
    headers = 'content-type, token' if '/editorRequests' in request.path else 'content-type'

    if request.method == 'OPTIONS':
        return create_response({}, 200, '*', headers)

    return None


@user_url.route('', methods=['POST', 'OPTIONS'])
def register():
    """
    Try to add new user to database
    if status 400 returns json (at least one field):
        'name': given_name
        'email': given_email
        'password': given_password
    :return: registration success status and json of what went wrong if unsuccessful
    """
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    editor_request = request.json['editorRequest']

    data = {}
    if len(name) < 3 or len(name) > 30:
        data['error'] = 'Nieprawidłowe imię, musi mieć od 3 do 30 znaków'

    if not email.endswith('agh.edu.pl'):
        data['error'] = 'Nieprawidłowy email, musi się kończyć agh.edu.pl'
    elif len(email) > 30:
        data['error'] = 'Nieprawidłowy email, musi mieć mniej niż 30 znaków'
    elif '@' not in email:
        data['error'] = 'Nieprawidłowy email, musi posiadać znak @'

    if len(password) < 3 or len(password) > 30:
        data['error'] = 'Nieprawdiłowe hasło, musi mieć od 3 do 30 znaków'

    if len(data) > 0:
        return create_response(data, 400, '*')

    check_user = User.query.filter_by(email=email).first()

    if check_user:
        return create_response({'error': 'Podany adres email jest już zajęty'}, 409, '*')

    is_admin = email.endswith('@admin.agh.edu.pl')

    new_user = User(email, name, password, is_admin)
    db.session.add(new_user)

    if editor_request and not is_admin:
        new_editor_request = EditorRequest(email, name)
        db.session.add(new_editor_request)

    db.session.commit()

    return create_response({}, 200, '*')


@user_url.route('/auth', methods=['POST', 'OPTIONS'])
def login():
    """
    Try to login user+
    if status 200 returns json {'role': user_role} and sets response cookie - 'email': email
    :return: login success status and user role if successful
    """
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if user and user.verify_password(password):
        if user.email.endswith('@admin.agh.edu.pl'):
            role = 'admin'
        elif user.is_editor:
            role = 'editor'
        else:
            role = 'user'

        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(minutes=30),
            'iat': datetime.utcnow(),
            'role': role
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        data = {
            'role': role,
            'token': token
        }
        status = 200
    else:
        if not user:
            data = {'error': 'Nie ma użytkownika o takim adresie email'}
        else:
            data = {'error': 'Nieprawidłowe hasło'}

        status = 400

    return create_response(data, status, '*')


@user_url.route('/editorRequests', methods=['GET', 'POST', 'OPTIONS'])
def admin_editor_requests():
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

    if role != 'admin':
        return create_response({'error': 'Tylko admin ma do tego dostęp'}, 403, '*')

    if request.method == 'POST':
        email = request.json['email']
        name = request.json['name']
        approval = request.json['approval']

        check_user = User.query.filter_by(email=email).first()
        check_editor_request = EditorRequest.query.filter_by(user_email=email).first()

        data = None
        if not check_user:
            data = {'error': 'Nie ma użytkownika o podanym adresie email'}
        elif not check_editor_request:
            data = {'error': 'Nie ma podania o edytora z takim adresem email'}
        elif check_user.name != name or check_editor_request.name != name:
            data = {'error': 'Podane imię jest niepoprawne'}
        elif approval not in ['accept', 'reject']:
            data = {'error': 'Niepoprawny status podania, musi być accept lub reject'}

        if data is not None:
            return create_response(data, 409, '*')

        if approval == 'accept':
            check_user.is_editor = True
        db.session.delete(check_editor_request)
        db.session.commit()

        return create_response({}, 200, '*')

    editor_requests = EditorRequest.query.all()
    data = [{'name': u.name, 'email': u.user_email} for u in editor_requests]

    return create_response(data, 200, '*')
