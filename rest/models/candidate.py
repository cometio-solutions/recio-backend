import enum
from rest.db import db


class Mode(enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"


class Candidate(db.Model):
    __tablename__ = 'candidate'
    pesel = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    region = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    highschool = db.Column(db.String(30), nullable=False)
    highschool_city = db.Column(db.String(30), nullable=False)
    matura_date = db.Column(db.DateTime, nullable=False)
    graduation_date = db.Column(db.DateTime)
    college_name = db.Column(db.String(30))
    faculty = db.Column(db.String(30))
    field_of_study = db.Column(db.String(30))
    mode = db.Column(db.Enum(Mode))
    average = db.Column(db.Float)

    def __repr__(self):
        return f'<Candidate(pesel={self.pesel}, name={self.name}, city={self.city},'\
            f' region={self.region}, country={self.country}, highschool={self.highschool}, '\
            f' highschool_city={self.highschool_city}, matura_date={self.matura_date}, '\
            f' graduation_date={self.graduation_date}, college_name={self.college_name}, '\
            f' faculty={self.faculty}, field_of_study={self.field_of_study}, mode={self.mode}, '\
            f' average={self.average})>'
