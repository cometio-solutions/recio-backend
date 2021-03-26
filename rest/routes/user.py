import json
import re
from flask import request, Blueprint, Response
from rest.db import db
from rest.models.user import User
from rest.models.editor_request import EditorRequest


user_url = Blueprint('user', __name__)


@user_url.route('/', methods=['POST'])
def register():
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

    new_user = User(email, name, password, False)
    db.session.add(new_user)

    if editor_request:
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
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        data = {'auth': True}
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


@user_url.route('/editorRequests', methods=['GET'])
def admin_editor_requests():
    if 'email' not in request.cookies:
        status = 401
        data = {'cookie': False}
    else:
        email = request.cookies.get('email')
        user = User.query.filter_by(email=email).first()

        if not user or not email == 'admin@admin.agh.edu.pl':
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
