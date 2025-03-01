from datetime import datetime
from models import db

class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    query = db.Column(db.String(255), nullable=False)
    num_results = db.Column(db.Integer, nullable=False)
