import enum
from rest.db import db


class RecruitmenStatus(enum.Enum):
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT_QUALIFIED"


class CandidateRecruitment(db.Model):
    __tablename__ = 'candidateRecruitment'
    id = db.Column(db.Integer, primary_key=True)
    recruitment_id = db.Column(db.Integer, db.ForeignKey('recruitment.id'), nullable=False)
    candidate_pesel = db.Column(db.Integer, db.ForeignKey('candidate.pesel'), nullable=False)
    is_paid = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Enum(RecruitmenStatus))
    points = db.Column(db.Integer)
    test_points = db.Column(db.Integer)

    recruitment = db.relationship('Recruitment', backref=db.backref('candidate_recruitments',
                                  lazy=True))
    candidate = db.relationship('Candidate', backref=db.backref('recruitments',
                                lazy=True))

    def __repr__(self):
        return f'<CandidateRecruitment(id={self.id}, recruitment_id={self.recruitment_id}, '\
            f'candidate_pesel={self.candidate_pesel}, is_paid={self.is_paid}, status={self.status}'\
            f', points={self.points}, test_points={self.test_points})>'
