"""This module stores Recruitment model"""
from rest.db import db


class Recruitment(db.Model):
    """
    This class coresponds to recruitment table in database.
    It stores data about recruitment for given major
    """
    __tablename__ = 'recruitment'
    id = db.Column(db.Integer, primary_key=True)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'),
                         nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    cycle_number = db.Column(db.Integer, nullable=False)
    slot_limit = db.Column(db.Integer, nullable=False)
    point_limit = db.Column(db.Integer, nullable=False)

    major = db.relationship('Major', backref=db.backref('recruitments', lazy=True))

    def __repr__(self):
        return f'<Recruitment(id={self.id}, major_id={self.major_id}, end_date={self.end_date},'\
            f' cycle_number={self.cycle_number}, slot_limit={self.slot_limit},'\
            f' point_limit={self.point_limit})>'
