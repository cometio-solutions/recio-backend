from datetime import datetime
import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.environ["USER"]}:' \
    f'{os.environ["PASSWORD"]}@{os.environ["HOST"]}:{os.environ["PORT"]}/{os.environ["DATABASE"]}'
db = SQLAlchemy(app)

from rest.models.user import User
from rest.models.editor_request import EditorRequest
from rest.models.major import Major
from rest.models.recruitment import Recruitment
from rest.models.candidate import Candidate
from rest.models.matura_result import MaturaResult
from rest.models.candidate_recruitment import CandidateRecruitment

db.drop_all()
db.create_all()
db.session.commit()
# example
admin = User("admin@admin.agh.edu.pl", "admin", "admin", True)
cs = Major(name="Informatyka", faculty="WIET", degree="BACHELOR", mode="FULL_TIME")
r = Recruitment(end_date=datetime.now(), cycle_number=1, point_limit=920, slot_limit=300)
cs.recruitments.append(r)
db.session.add(admin)
db.session.add(cs)
db.session.commit()


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
