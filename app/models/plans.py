from models import db

class Plan(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    num_queries = db.Column(db.Integer, nullable=False)

    user_plans = db.relationship('UserPlan', backref='plan', lazy=True)
