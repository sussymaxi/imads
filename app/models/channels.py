from models import db

class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    id_channel = db.Column(db.String(50), unique=True, nullable=False)
    url = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(255), nullable=True)

    products = db.relationship('Product', backref='channel', lazy=True)
