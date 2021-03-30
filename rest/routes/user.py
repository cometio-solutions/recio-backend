import re
from datetime import datetime, timedelta
import jwt
from flask import request, Blueprint, current_app
from rest.db import db
from rest.models.user import User
from rest.models.editor_request import EditorRequest
from rest.common.response import create_response


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
    if len(name) < 3 or len(name) > 30 or re.match('^[.a-zA-Z0-9_-]+$', name) is None:
        data['name'] = name
    if not email.endswith('agh.edu.pl') or re.match('^[.@a-zA-Z0-9_-]+$', email) is None:
        data['email'] = email
    if len(password) < 3 or len(password) > 30 or re.match('^[.a-zA-Z0-9_-]+$', password) is None:
        data['password'] = password

    if len(data) > 0:
        return create_response(data, 400, '*')

    check_user = User.query.filter_by(email=email).first()

    if check_user:
        return create_response({}, 409, '*')

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

    if user and user.password == password:
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
        data = {}
        status = 400

    return create_response(data, status, '*')


@user_url.route('/editorRequests', methods=['GET', 'POST', 'OPTIONS'])
def admin_editor_requests():
    """
    Either get (GET) editor requests or give (POST) user editor status
    Requires 'email' field in cookies.
    if method GET and status 200 returns json:
        list of [
            'name': name
            'email': email
        ]
    :return: success status and json editor requests (if GET)
    """
    if 'token' not in request.headers:
        return create_response({'message': 'No token found, log in!'}, 401, '*')

    try:
        token = jwt.decode(
            request.headers['token'],
            current_app.config['SECRET_KEY'],
            algorithms='HS256'
        )
    except jwt.ExpiredSignatureError:
        return create_response({'message': 'Token expired, log in again!'}, 401, '*')
    except jwt.InvalidSignatureError:
        return create_response({'message': 'Invalid token signature!'}, 401, '*')

    role = token['role']

    if role != 'admin':
        return create_response({}, 403, '*')

    if request.method == 'POST':
        email = request.json['email']
        name = request.json['name']

        check_user = User.query.filter_by(email=email).first()
        check_editor_request = EditorRequest.query.filter_by(user_email=email).first()

        if not check_user or not check_editor_request or \
                check_user.name != name or check_editor_request.name != name:
            status = 409
        else:
            check_user.is_editor = True
            db.session.delete(check_editor_request)
            db.session.commit()

            status = 200

        return create_response({}, status, '*')

    editor_requests = EditorRequest.query.all()
    data = [{'name': u.name, 'email': u.user_email} for u in editor_requests]

    return create_response(data, 200, '*')
