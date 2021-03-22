from datetime import datetime
import os
from flask import Flask
from rest.db import db
from rest.models.user import User
from rest.models.editor_request import EditorRequest
from rest.models.major import Major
from rest.models.recruitment import Recruitment
from rest.models.candidate import Candidate
from rest.models.matura_result import MaturaResult
from rest.models.candidate_recruitment import CandidateRecruitment


def create_app():
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ["USER"]}:' \
        f'{os.environ["PASSWORD"]}@{os.environ["HOST"]}:{os.environ["PORT"]}/'\
        f'{os.environ["DATABASE"]}'
    db.init_app(app)
    print("App created")
    return app


def setup_database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
        print("Created database schema")
        # example
        admin = User("admin@admin.agh.edu.pl", "admin", "admin", True)
        cs_major = Major(name="Informatyka", faculty="WIET", degree="BACHELOR", mode="FULL_TIME")
        cs_recruitment = Recruitment(end_date=datetime.now(), cycle_number=1, point_limit=920,
                                     slot_limit=300)
        cs_major.recruitments.append(cs_recruitment)
        db.session.add(admin)
        db.session.add(cs_major)
        db.session.commit()
        print(User.query.all())
        print(Major.query.all())
        print(Recruitment.query.all())
        print(EditorRequest.query.all())
        print(Candidate.query.all())
        print(MaturaResult.query.all())
        print(CandidateRecruitment.query.all())
