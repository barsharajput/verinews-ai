from flask_login import UserMixin

from database.db import db

print("Models loaded")


# USER TABLE
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(20))
    country = db.Column(db.String(100))

    password = db.Column(db.String(200), nullable=False)


# HISTORY TABLE
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    result = db.Column(db.String(10))
    confidence = db.Column(db.Float)
    user_id = db.Column(db.Integer)
