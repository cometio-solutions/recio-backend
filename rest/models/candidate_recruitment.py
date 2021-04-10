"""This module stores Candidate Recruitment model"""
import enum
from rest.db import db


class RecruitmenStatus(enum.Enum):
    """
    Candidate can be either QUALIFIED or NOT_QUALIFIED
    """
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT_QUALIFIED"


class CandidateRecruitment(db.Model):
    """
    This class coresponds to candidateRecruitment table in database.
    It describes a candidate recruitment and stores data connected with recruitment proccess
    """
    __tablename__ = 'candidateRecruitment'
    id = db.Column(db.Integer, primary_key=True)
    recruitment_id = db.Column(db.Integer, db.ForeignKey('recruitment.id'), nullable=False)
    candidate_pesel = db.Column(db.String(30), db.ForeignKey('candidate.pesel'), nullable=False)
    is_paid = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Enum(RecruitmenStatus))
    points = db.Column(db.Integer)
    test_points = db.Column(db.Integer)

    recruitment = db.relationship('Recruitment', backref=db.backref('candidate_recruitments',
                                  lazy=True))
    candidate = db.relationship('Candidate', backref=db.backref('recruitments',
                                lazy=True))

    @classmethod
    def from_dict(cls, candidate_dict):
        """
        Creates CandidateRecruitment from dict
        :param candidate_dict: dictionary with fields: test_result, is_paid, matura_result, average
        :return: CandidateRecruitment object
        """
        # forget to add is_paid to generator, will be added in the next sprint
        test_points = None
        points = None
        if candidate_dict['test_result'] is not None and candidate_dict['average'] is not None:
            test_points = int(candidate_dict['test_result'])
            average = float(candidate_dict['average'])
            points = int(int(20*average) + test_points)
        else:
            points = int(candidate_dict['matura_result'])
        return CandidateRecruitment(is_paid=True, points=points, test_points=test_points)

    def __repr__(self):
        return f'<CandidateRecruitment(id={self.id}, recruitment_id={self.recruitment_id}, '\
            f'candidate_pesel={self.candidate_pesel}, is_paid={self.is_paid}, status={self.status}'\
            f', points={self.points}, test_points={self.test_points})>'
