from datetime import datetime
from models import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(512), nullable=True)
    price_old = db.Column(db.Float, nullable=True)
    price_new = db.Column(db.Float, nullable=True)
    status = db.Column(db.Boolean, default=True)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    date_update = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    id_post = db.Column(db.String(32), nullable=True)
    id_channel = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=True)
