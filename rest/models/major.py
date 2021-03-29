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
    faculty = db.Column(db.String(30), nullable=False)
    degree = db.Column(db.Enum(Degree), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    mode = db.Column(db.Enum(Mode), nullable=False)

    def __repr__(self):
        return f'<Major(id={self.id}, faculty={self.faculty}, degree={self.degree}, '\
            f'name={self.name}, mode={self.mode})>'
