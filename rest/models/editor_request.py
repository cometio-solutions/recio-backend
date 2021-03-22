from rest.db import db


class EditorRequest(db.Model):
    __tablename__ = 'editorRequest'
    user_email = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, email, name):
        self.user_email = email
        self.name = name

    def __repr__(self):
        return f'<EditorRequest(userEmail={self.user_email}, name={self.name})>'
