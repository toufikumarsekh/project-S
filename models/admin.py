from flask_login import UserMixin
from models.inquiry import db

class Admin(UserMixin, db.Model):

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )