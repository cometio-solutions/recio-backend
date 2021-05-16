"""This module stores Candidate model"""
import enum
from rest.db import db
from rest.common.date import datetime_from_string


class Mode(enum.Enum):
    """
    There are two two types of studies mode:
    FULL_TIME and PART_TIME
    """
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"

    def __str__(self):
        if str(self.value) == "FULL_TIME":
            return "Studia dzienne"
        if str(self.value) == "PART_TIME":
            return "Studia zaoczne"

        return "Studia"


class Candidate(db.Model):
    """
    This class coresponds to candidate table in database.
    It describes a candidate to college.
    """
    __tablename__ = 'candidate'
    pesel = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    region = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    highschool = db.Column(db.String(30), nullable=False)
    highschool_city = db.Column(db.String(30), nullable=False)
    matura_date = db.Column(db.DateTime, nullable=False)
    matura_points = db.Column(db.Integer, nullable=False)
    graduation_date = db.Column(db.DateTime)
    college_name = db.Column(db.String(50))
    faculty = db.Column(db.String(50))
    field_of_study = db.Column(db.String(50))
    mode = db.Column(db.Enum(Mode))
    average = db.Column(db.Float)

    @classmethod
    def from_dict(cls, candidate_dict):
        """
        Creates Candidate from dict
        :param candidate_dict: dictionary with fields: pesel, name, city,region, country,
        highschool, highschool_city, matura_date, matura_result,
        graduation_date, college_name, faculty, field_of_study, mode,average,
        :return: Candidate object
        """
        graduation_date = None
        average = None
        if candidate_dict['graduation_date']:
            graduation_date = datetime_from_string(candidate_dict['graduation_date'])
        if candidate_dict['average']:
            average = float(candidate_dict['average'])
        return Candidate(pesel=candidate_dict['pesel'], name=candidate_dict['name'],
                         city=candidate_dict['city'], region=candidate_dict['region'],
                         country=candidate_dict['country'], highschool=candidate_dict['highschool'],
                         highschool_city=candidate_dict['highschool_city'],
                         matura_date=datetime_from_string(candidate_dict['matura_date']),
                         matura_points=int(candidate_dict['matura_result']),
                         graduation_date=graduation_date,
                         college_name=candidate_dict['college_name'],
                         faculty=candidate_dict['faculty'],
                         field_of_study=candidate_dict['field_of_study'],
                         mode=candidate_dict['mode'], average=average)

    def add_college(self, candidate_dict):
        """
        Adds college data for candidate
        :param candidate_dict: dictionary with fields:
        graduation_date, college_name, faculty, field_of_study, mode,average,
        """
        self.college_name = candidate_dict['college_name']
        self.faculty = candidate_dict['faculty']
        self.field_of_study = candidate_dict['field_of_study']
        self.mode = candidate_dict['mode']
        self.average = float(candidate_dict['average'])
        self.graduation_date = datetime_from_string(candidate_dict['graduation_date'])

    @staticmethod
    def to_json(candidate):
        """
        Return json for given candidate
        :param candidate: candidate object from database
        :return: A parsed json object with candidate data
        """
        return {
            "pesel": candidate.pesel,
            "name": candidate.name,
            "city": candidate.city,
            "region": candidate.region,
            "country": candidate.country,
            "highschool": candidate.highschool,
            "highschool_city": candidate.highschool_city,
            "matura_date": candidate.matura_date.strftime("%m/%d/%Y, %H:%M:%S"),
            "matura_points": candidate.matura_points,
            "graduation_date": candidate.graduation_date,
            "college_name": candidate.college_name,
            "faculty": candidate.faculty,
            "field_of_study": candidate.field_of_study,
            "mode": str(candidate.mode),
            "average": candidate.average,
        }

    def __repr__(self):
        return f'<Candidate(pesel={self.pesel}, name={self.name}, city={self.city},' \
               f' region={self.region}, country={self.country}, highschool={self.highschool}, ' \
               f' highschool_city={self.highschool_city}, matura_date={self.matura_date}, ' \
               f' graduation_date={self.graduation_date}, college_name={self.college_name}, ' \
               f' faculty={self.faculty}, field_of_study={self.field_of_study}, mode={self.mode}, '\
               f' average={self.average})>'
