"""This module stores User model"""
from werkzeug.security import generate_password_hash, check_password_hash
from rest.db import db


class User(db.Model):
    """
    This class coresponds to user table in database.
    It stores data about user of our app
    """
    __tablename__ = 'user'
    email = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(120))
    is_editor = db.Column(db.Boolean)

    def __init__(self, email, name, password, is_editor):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)
        self.is_editor = is_editor

    def __repr__(self):
        return f'<User(email={self.email}, name={self.name}, isEditor={self.is_editor})>'

    def verify_password(self, pwd):
        """
        Cheks if password matched with password hash in the database
        :paran pwd: plaintext password to compare
        :return: True if password matched, False otherwise
        """
        return check_password_hash(self.password, pwd)
