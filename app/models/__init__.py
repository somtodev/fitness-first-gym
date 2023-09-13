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


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    schedule = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('packages', lazy='dynamic'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    trainer = db.relationship('Trainer', backref=db.backref('package', lazy='dynamic'))
    current_capacity = db.Column(db.Integer, default=0)
    max_capacity = db.Colum(db.Integer, default=10)


class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('packages', lazy='dynamic'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)