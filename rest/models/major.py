"""This module stores Major model"""
import enum
from rest.models.candidate import Mode
from rest.db import db


class Degree(enum.Enum):
    """
    There are two types of studies:
    BACHELOR or MASTER
    """
    BACHELOR = "BACHELOR"
    MASTER = "MASTER"


class Major(db.Model):
    """
    This class coresponds to major table in database.
    It describes a major (field of study) in which the candidate can be recruited
    """
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.Enum(Degree), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    mode = db.Column(db.Enum(Mode), nullable=False)

    @classmethod
    def from_dict(cls, major_dict):
        """
        Creates Major from dict
        :param major_dict: dictionary with fields: faculty, degree, major_name, mode
        :return: Major object
        """
        return Major(faculty=major_dict['faculty'], degree=major_dict['degree'],
                     name=major_dict['major_name'], mode=major_dict['mode'])

    def __repr__(self):
        return f'<Major(id={self.id}, faculty={self.faculty}, degree={self.degree}, '\
            f'name={self.name}, mode={self.mode})>'
