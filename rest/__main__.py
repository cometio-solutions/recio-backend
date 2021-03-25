import json
import re
from rest.app import create_app, setup_database
from rest.models.user import User
from rest.models.editor_request import EditorRequest
from rest.db import db
from flask import request


app = create_app()
setup_database(app)


@app.route('/')
def hello():
    data = {"app": "recio"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/user', methods=['POST'])
def register():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    editor_request = request.form.get('editorRequest')

    data = {}
    if len(name) < 3 or len(name) > 30 or re.match('^[.a-zA-Z0-9_-]+$', name) is None:
        data["invalid_name"] = name
    if not email.endswith('agh.edu.pl') or re.match('^[.@a-zA-Z0-9_-]+$', email) is None:
        data["invalid_email"] = email
    if len(password) < 3 or len(password) > 30 or re.match('^[.a-zA-Z0-9_-]+$', password) is None:
        data["invalid_password"] = password

    if len(data) > 0:
        response = app.response_class(
            response=json.dumps(data),
            status=400,
            mimetype='application/json'
        )
        return response

    check_user = User.query.filter_by(email=email).first()

    if check_user:
        response = app.response_class(
            response=json.dumps({"email_taken": email}),
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

    response = app.response_class(
        response=json.dumps({"name": name, "email": email, "password": password, "editorRequest": editor_request}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/user/auth', methods=['POST'])
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

    response = app.response_class(
            response=json.dumps(data),
            status=status,
            mimetype='application/json'
        )
    if status == 200:
        response.set_cookie('email', value=email)

    return response


@app.route('/user/editorRequests', methods=['GET'])
def admin_editor_requests():
    if 'email' not in request.cookies:
        return app.response_class(response=json.dumps({'cookie': False}), status=401, mimetype='application/json')

    email = request.cookies.get('email')
    user = User.query.filter_by(email=email).first()

    if not user or not user.is_editor:
        return app.response_class(response=json.dumps({'is_editor': False}), status=403, mimetype='application/json')

    users = User.query.all()
    data = [{'name': u.name, 'user_email': u.email} for u in users]

    return app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )


app.run(host='0.0.0.0')
