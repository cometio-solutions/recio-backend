from rest.db import db


class MaturaResult(db.Model):
    __tablename__ = 'maturaResult'
    id = db.Column(db.Integer, primary_key=True)
    candidate_pesel = db.Column(db.Integer, db.ForeignKey('candidate.pesel'),
                                nullable=False)
    subject_name = db.Column(db.String(30), nullable=False)
    result = db.Column(db.Float, nullable=False)

    candidate = db.relationship('Candidate', backref=db.backref('matura_results', lazy=True))

    def __repr__(self):
        return f'<MaturaResult(id={self.id}, candidate_pesel={self.candidate_pesel}, '\
            f'subject_name={self.subject_name}, result={self.result})>'
