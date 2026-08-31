from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Inquiry(db.Model):
    __tablename__ = "inquiries"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(20), nullable=False)

    email = db.Column(db.String(120))

    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )