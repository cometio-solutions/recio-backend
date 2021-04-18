"""This module stores Recruitment model"""
from datetime import datetime
from rest.common.date import datetime_from_string
from rest.db import db


class Recruitment(db.Model):
    """
    This class corresponds to recruitment table in database.
    It stores data about recruitment for given major
    """
    __tablename__ = 'recruitment'
    id = db.Column(db.Integer, primary_key=True)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'),
                         nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    cycle_number = db.Column(db.Integer, nullable=False)
    slot_limit = db.Column(db.Integer, nullable=False)
    point_limit = db.Column(db.Integer)

    major = db.relationship('Major', backref=db.backref('recruitments', lazy=True))

    @classmethod
    def from_dict(cls, recruitment_dict):
        """
        Creates Recruitment from dict
        :param recruitment_dict: dictionary with fields: end_date, slot_limit, cycle_number
        :return: Recruitment object
        """
        return Recruitment(end_date=datetime_from_string(recruitment_dict['end_date']),
                           cycle_number=int(recruitment_dict['cycle_number']),
                           slot_limit=int(recruitment_dict['slot_limit']))

    def __repr__(self):
        return f'<Recruitment(id={self.id}, major_id={self.major_id}, end_date={self.end_date},' \
               f' cycle_number={self.cycle_number}, slot_limit={self.slot_limit},' \
               f' point_limit={self.point_limit})>'

    @staticmethod
    def to_json(rec, candidates_num):
        """
        Return json for recruitment data
        :param candidates_num: int
        :param rec: Recruitment
        :return: recruitment dict
        """
        return {
            'id': rec.id,
            'major_id': rec.major_id,
            'end_date': rec.end_date.strftime("%m/%d/%Y, %H:%M:%S"),
            'cycle_number': rec.cycle_number,
            'slot_limit': rec.slot_limit,
            'candidates_num': candidates_num,
            'point_limit': rec.point_limit,
            'is_active': bool(rec.end_date > datetime.now()),
            'faculty': rec.major.faculty,
            'degree': str(rec.major.degree),
            'major_name': rec.major.name,
            'major_mode': str(rec.major.mode)
        }
