from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Use SQLite for simplicity; replace with your actual database URL
db = SQLAlchemy(app)

# Define the SubscriptionPackages model
class SubscriptionPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(255))
    monthly_fee = db.Column(db.Float)

# Define the Classes model
class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(255))
    package_id = db.Column(db.Integer, db.ForeignKey('subscription_package.id'))
    package = db.relationship('SubscriptionPackage', backref='classes')

# Define the TrainerBookings model
class TrainerBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.id'))
    booking_date = db.Column(db.Date)
    package_id = db.Column(db.Integer, db.ForeignKey('subscription_package.id'))
    member = db.relationship('Member', backref='trainer_bookings')
    trainer = db.relationship('Trainer', backref='member_bookings')
    package = db.relationship('SubscriptionPackage', backref='bookings')

# Define the Member model
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add other member-related fields as needed

# Define the Trainer model
class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add other trainer-related fields as needed
