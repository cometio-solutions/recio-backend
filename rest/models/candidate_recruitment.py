"""This module stores Candidate Recruitment model"""
import enum
from rest.db import db


class RecruitmentStatus(enum.Enum):
    """
    Candidate can be either QUALIFIED or NOT_QUALIFIED
    """
    QUALIFIED = "ZAKWALIFIKOWANY"
    NOT_QUALIFIED = "NIE ZAKWALIFIKOWANY"


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
    status = db.Column(db.Enum(RecruitmentStatus))
    points = db.Column(db.Integer, nullable=False)
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
        if candidate_dict['test_result'] and candidate_dict['average']:
            test_points = int(candidate_dict['test_result'])
            average = float(candidate_dict['average'])
            points = int(int(20*average) + test_points)
        else:
            points = int(candidate_dict['matura_result'])
        return CandidateRecruitment(is_paid=bool(int(candidate_dict['is_paid'])),
                                    points=points, test_points=test_points)

    def __repr__(self):
        return f'<CandidateRecruitment(id={self.id}, recruitment_id={self.recruitment_id}, '\
            f'candidate_pesel={self.candidate_pesel}, is_paid={self.is_paid}, status={self.status}'\
            f', points={self.points}, test_points={self.test_points})>'

    @staticmethod
    def to_json(rec):
        """
        Return json for candidate recruitment data
        :param rec: candidate recruitment
        :return: dict with candidate recruitment
        """
        graduation_date = None
        status = None
        if rec.candidate.graduation_date:
            graduation_date = rec.candidate.graduation_date.strftime("%m/%d/%Y, %H:%M:%S")
        if rec.status:
            status = rec.status.value
        return {
            'candidate_recruitment_id': rec.id,
            'is_paid': rec.is_paid,
            'status': status,
            'points': rec.points,
            'test_points': rec.test_points,
            'pesel': rec.candidate.pesel,
            'name': rec.candidate.name,
            "city": rec.candidate.city,
            "region": rec.candidate.region,
            "country": rec.candidate.country,
            "highschool": rec.candidate.highschool,
            "highschool_city": rec.candidate.highschool_city,
            "matura_date": rec.candidate.matura_date.strftime("%m/%d/%Y, %H:%M:%S"),
            "matura_points": rec.candidate.matura_points,
            "graduation_date": graduation_date,
            "college_name": rec.candidate.college_name,
            'faculty': rec.candidate.faculty,
            'field_of_study': rec.candidate.field_of_study,
            'mode': rec.candidate.mode,
            'average': rec.candidate.average
        }
