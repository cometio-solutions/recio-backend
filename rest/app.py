"""This module creates recio app and setups database"""
import os
from flask import Flask
from rest.db import db
from rest.models.user import User
from rest.models.editor_request import EditorRequest
from rest.models.major import Major
from rest.models.recruitment import Recruitment
from rest.models.candidate import Candidate
from rest.models.candidate_recruitment import CandidateRecruitment
from rest.routes.recruitment import recruitment_url
from rest.routes.user import user_url
from rest.routes.file import file_url
from rest.routes.health_check import healthcheck_url


def create_app():
    """
    This method creates flask app, sets config and conects to database
    :returns: created flask app
    """
    app = Flask(__name__)
    app.register_blueprint(user_url, url_prefix='/user')
    app.register_blueprint(recruitment_url, url_prefix='/recruitment')
    app.register_blueprint(file_url, url_prefix='/file')
    app.register_blueprint(healthcheck_url, url_prefix='/healthcheck')
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ["USER"]}:' \
        f'{os.environ["PASSWORD"]}@{os.environ["HOST"]}:{os.environ["PORT"]}/'\
        f'{os.environ["DATABASE"]}'
    db.init_app(app)
    print("App created")
    return app


def setup_database(app):
    """
    This method setups database.
    First all tables are droped and then new ones are created.
    At the end some example data are added into database
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        print("Created database schema")
        # example
        admin = User("admin@admin.agh.edu.pl", "admin", "admin", True)
        editor = User("editor@agh.edu.pl", "editor", "editor", True)
        db.session.add(admin)
        db.session.add(editor)
        db.session.commit()
        print(User.query.all())
        print(Major.query.all())
        print(Recruitment.query.all())
        print(EditorRequest.query.all())
        print(Candidate.query.all())
        print(CandidateRecruitment.query.all())
