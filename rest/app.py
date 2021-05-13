"""This module creates recio app and setups database"""
import os
import logging
from flask import Flask
from rest.db import db
from rest.models.user import User
from rest.models.editor_request import EditorRequest
from rest.models.major import Major
from rest.models.recruitment import Recruitment
from rest.models.candidate import Candidate
from rest.models.candidate_recruitment import CandidateRecruitment
from rest.routes.candidate import candidate_url
from rest.routes.recruitment import recruitment_url
from rest.routes.user import user_url
from rest.routes.file import file_url
from rest.routes.health_check import healthcheck_url
from rest.routes.point_limit import point_limit_url
from rest.routes.years import years_url
from rest.routes.majors import majors_url
from rest.routes.origins import origins_url
from rest.routes.points_sum import points_sum_url


def create_app():
    """
    This method creates flask app, sets config and conects to database
    :returns: created flask app
    """
    logging.info("Creating flask app")
    app = Flask(__name__)

    logging.info("Registering blueprints")
    app.register_blueprint(user_url, url_prefix='/user')
    app.register_blueprint(recruitment_url, url_prefix='/recruitment')
    app.register_blueprint(file_url, url_prefix='/file')
    app.register_blueprint(healthcheck_url, url_prefix='/healthcheck')
    app.register_blueprint(point_limit_url, url_prefix='/point-limit')
    app.register_blueprint(years_url, url_prefix='/years')
    app.register_blueprint(majors_url, url_prefix='/majors')
    app.register_blueprint(origins_url, url_prefix='/origins')
    app.register_blueprint(points_sum_url, url_prefix='/points')
    app.register_blueprint(candidate_url, url_prefix='/candidate')

    logging.info("Getting secrets")
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ["USER"]}:' \
        f'{os.environ["PASSWORD"]}@{os.environ["HOST"]}:{os.environ["PORT"]}/'\
        f'{os.environ["DATABASE"]}'
    db.init_app(app)
    logging.info("App created properly!")
    return app


def setup_database(app):
    """
    This method setups database.
    First all tables are droped and then new ones are created.
    At the end some example data are added into database
    """
    logging.info("Setting up database")
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        logging.info("Created database schema")
        # example
        admin = User("admin@admin.agh.edu.pl", "admin", "admin", True)
        editor = User("editor@agh.edu.pl", "editor", "editor", True)
        db.session.add(admin)
        db.session.add(editor)
        db.session.commit()
        logging.info(User.query.all())
        logging.info(Major.query.all())
        logging.info(Recruitment.query.all())
        logging.info(EditorRequest.query.all())
        logging.info(Candidate.query.all())
        logging.info(CandidateRecruitment.query.all())
