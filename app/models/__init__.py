from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login_manager   


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)   
    lastname = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    isAdmin = db.Column(db.Boolean(), default=False)
    membership_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=True)
    membership = db.relationship('Package', backref=db.backref('packages', lazy='dynamic'))
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.email


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)