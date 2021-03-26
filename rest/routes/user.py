import json
import re
from flask import request, Blueprint, Response
from rest.db import db
from rest.models.user import User
from rest.models.editor_request import EditorRequest

user_url = Blueprint('user', __name__)


@user_url.route('/', methods=['POST'])
def register():
    """
    Try to add new user to database
    :return: registration success status and json of what went wrong if unsuccessful
    """
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    editor_request = request.form.get('editorRequest') == 'True'

    data = {}
    if len(name) < 3 or len(name) > 30 or re.match('^[.a-zA-Z0-9_-]+$', name) is None:
        data['invalid_name'] = name
    if not email.endswith('agh.edu.pl') or re.match('^[.@a-zA-Z0-9_-]+$', email) is None:
        data['invalid_email'] = email
    if len(password) < 3 or len(password) > 30 or re.match('^[.a-zA-Z0-9_-]+$', password) is None:
        data['invalid_password'] = password

    if len(data) > 0:
        response = Response(
            response=json.dumps(data),
            status=400,
            mimetype='application/json'
        )
        return response

    check_user = User.query.filter_by(email=email).first()

    if check_user:
        response = Response(
            response=json.dumps({'email_taken': email}),
            status=409,
            mimetype='application/json'
        )
        return response

    is_admin = email.endswith('@admin.agh.edu.pl')

    new_user = User(email, name, password, is_admin)
    db.session.add(new_user)

    if editor_request and not is_admin:
        new_editor_request = EditorRequest(email, name)
        db.session.add(new_editor_request)

    db.session.commit()

    response = Response(
        response=json.dumps({}),
        status=200,
        mimetype='application/json'
    )
    return response


@user_url.route('/auth', methods=['POST'])
def login():
    """
    Try to login user
    :return: login success status and user role if successful
    """
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        if user.email.endswith('@admin.agh.edu.pl'):
            role = 'admin'
        elif user.is_editor:
            role = 'editor'
        else:
            role = 'user'

        data = {'auth': True, 'role': role}
        status = 200
    else:
        data = {'auth': False}
        status = 400

    response = Response(
        response=json.dumps(data),
        status=status,
        mimetype='application/json'
    )
    if status == 200:
        response.set_cookie('email', value=email)

    return response


@user_url.route('/editorRequests', methods=['GET', 'POST'])
def admin_editor_requests():
    """
    Either get (GET) editor requests or give (POST) user editor status
    :return: success status and json editor requests (if GET)
    """
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')

        check_user = User.query.filter_by(email=email).first()
        check_editor_request = EditorRequest.query.filter_by(user_email=email).first()

        if not check_user or not check_editor_request or \
                check_user.name != name or check_editor_request.name != name:
            status = 400
            data = {'data': 'invalid'}
        else:
            check_user.is_editor = True
            db.session.delete(check_editor_request)
            db.session.commit()

            status = 200
            data = {'data': 'valid', 'is_editor': check_user.is_editor}

        return Response(
            response=json.dumps(data),
            status=status,
            mimetype='application/json'
        )

    if 'email' not in request.cookies:
        status = 401
        data = {'cookie': False}
    else:
        email = request.cookies.get('email')
        user = User.query.filter_by(email=email).first()

        if not user or not email.endswith('@admin.agh.edu.pl'):
            status = 403
            data = {'is_admin': False}
        else:
            status = 200
            editor_requests = EditorRequest.query.all()
            data = [{'name': u.name, 'user_email': u.user_email} for u in editor_requests]

    return Response(
        response=json.dumps(data),
        status=status,
        mimetype='application/json'
    )
