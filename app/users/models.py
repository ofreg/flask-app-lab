from app import db
from flask_login import UserMixin
class User(UserMixin,db.Model):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(120),unique=True, nullable=False)
    password=db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"Users('{self.email}')"