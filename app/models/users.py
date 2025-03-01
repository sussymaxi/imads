from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models.database import db
from models.history import History

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(68), unique=True, nullable=False)
    pass_hash = db.Column(db.String(32), nullable=False)

    user_plans = db.relationship('UserPlan', backref='user', lazy=True)
    history = db.relationship('History', backref='user', lazy=True)

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

class UserPlan(db.Model):
    __tablename__ = 'user_plans'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id_plan = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_end = db.Column(db.DateTime, nullable=False)
    auto_renew = db.Column(db.Boolean, default=False)
