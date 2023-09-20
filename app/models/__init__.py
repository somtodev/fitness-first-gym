from app import db
from datetime import datetime, date
from flask_login import UserMixin
from app import login_manager   


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)   
    lastname = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    isAdmin = db.Column(db.Boolean(), default=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    payment_details = db.relationship('PaymentDetails', uselist=False, back_populates='user')
    membership = db.relation('Membership', uselist=False, back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.email


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id')) 
    package = db.relationship('Package', backref=db.backref('member', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='membership')


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    schedule = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('class', lazy='dynamic'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    trainer = db.relationship('Trainer', backref=db.backref('class', lazy='dynamic'))
    current_capacity = db.Column(db.Integer, default=0)
    max_capacity = db.Column(db.Integer, default=10)


class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('trainer_category', lazy='dynamic'))


class PaymentDetails(db.Model):
    card_number = db.Column(db.String(20), nullable=False, primary_key=True)
    card_name  = db.Column(db.String(100), nullable=False)
    card_expiry_date = db.Column(db.Date, nullable=False)
    card_cvv = db.Column(db.String(4), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='payment_details')


class MembershipBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today())
    status = db.Column(db.String(50), default='PENDING')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    membership_id = db.Column(db.Integer, db.ForeignKey('membership.id'))
    membership = db.relationship('Membership', backref=db.backref('membership_booking', lazy='dynamic'))


class ClassBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today())
    status = db.Column(db.String(50), default='PENDING')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    class_details = db.relationship('Class', backref=db.backref('class_booking', lazy='dynamic'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
