from rest.app import db


class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(30))
    is_editor = db.Column(db.Boolean)

    def __init__(self, email, name, password, is_editor):
        self.email = email
        self.name = name
        self.password = password
        self.is_editor = is_editor

    def __repr__(self):
        return f'<User(email={self.email}, name={self.name}, isEditor={self.is_editor})>'
