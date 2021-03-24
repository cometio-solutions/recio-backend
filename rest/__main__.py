import json
from rest.app import create_app, setup_database


from flask import request, redirect, flash
from rest.models.user import User
from rest.db import db
import requests
import sys

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


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        if len(name) < 3 or len(name) > 30:
            flash("Name has to be between 3 and 30 characters")
            return redirect('/signup')

        if not email.endswith('agh.edu.pl'):
            flash("Only agh.edu.pl emails are accepted")
            return redirect('/signup')

        if len(name) < 3 or len(name) > 30:
            flash("Password has to be between 3 and 30 characters")
            return redirect('/signup')

        print("EMAIL:", email, file=sys.stderr)
        print("LOGIN:", name, file=sys.stderr)
        print("PASSWORD:", password, file=sys.stderr)

        user = User.query.filter_by(email=email).first()

        if user:
            print("Email address already exists", file=sys.stderr)
            flash('Email address already exists')
            return redirect('/signup')

        new_user = User(email, name, password, False)

        db.session.add(new_user)
        db.session.commit()
        print(User.query.all(), file=sys.stderr)

        return redirect('/')

    return 'signup'


@app.route('/test')
def test():
    dictToSend = {"email": "xd@xd", "name": "xd", "password": "xd1"}
    res = requests.post("http://0.0.0.0:5000/signup", data=dictToSend)
    return 'response from server: '


app.run(host='0.0.0.0')
