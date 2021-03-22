import enum
from rest.db import db


class Degree(enum.Enum):
    BACHELOR = "BACHELOR"
    MASTER = "MASTER"


class Mode(enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"


class Major(db.Model):
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(30), nullable=False)
    degree = db.Column(db.Enum(Degree), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    mode = db.Column(db.Enum(Mode), nullable=False)

    def __repr__(self):
        return f'<Major(id={self.id}, faculty={self.faculty}, degree={self.degree}, '\
            f'name={self.name}, mode={self.mode})>'
