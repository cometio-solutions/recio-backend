import json
import re
from flask import request, Blueprint, Response
from rest.db import db
from rest.models.user import User
from rest.models.editor_request import EditorRequest


user_url = Blueprint('user', __name__)


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
    if request.method == 'OPTIONS':
        response = Response(response=json.dumps({}), status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'content-type')
        return response

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
        response = Response(response=json.dumps(data), status=400, mimetype='application/json')
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    check_user = User.query.filter_by(email=email).first()

    if check_user:
        response = Response(response=json.dumps({}), status=409, mimetype='application/json')
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    is_admin = email.endswith('@admin.agh.edu.pl')

    new_user = User(email, name, password, is_admin)
    db.session.add(new_user)

    if editor_request and not is_admin:
        new_editor_request = EditorRequest(email, name)
        db.session.add(new_editor_request)

    db.session.commit()

    response = Response(response=json.dumps({}), status=200, mimetype='application/json')
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@user_url.route('/auth', methods=['POST', 'OPTIONS'])
def login():
    """
    Try to login user+
    if status 200 returns json {'role': user_role} and sets response cookie - 'email': email
    :return: login success status and user role if successful
    """
    if request.method == 'OPTIONS':
        response = Response(response=json.dumps({}), status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'content-type')
        return response

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

        data = {'role': role}
        status = 200
    else:
        data = {}
        status = 400

    response = Response(response=json.dumps(data), status=status, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    if status == 200:
        response.set_cookie('email', value=email)

    return response


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
    if request.method == 'OPTIONS':
        response = Response(response=json.dumps({}), status=200, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'email, content-type')
        return response

    if 'email' not in request.headers:
        response = Response(response=json.dumps({}), status=401, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    email = request.headers['email']
    user = User.query.filter_by(email=email).first()

    if not user or not email.endswith('@admin.agh.edu.pl'):
        response = Response(response=json.dumps({}), status=403, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

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

        response = Response(response=json.dumps({}), status=status, mimetype='application/json')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    editor_requests = EditorRequest.query.all()
    data = [{'name': u.name, 'email': u.user_email} for u in editor_requests]

    response = Response(response=json.dumps(data), status=200, mimetype='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
