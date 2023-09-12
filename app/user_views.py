from app import app
from flask import request, redirect, render_template, flash
from flask_login import login_required, current_user, login_user
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/user')
@login_required
def user():
    return 'User'


@app.route('/user/classes', methods=['GET'])
@login_required
def userClasses():
    return 'User Classes'


@app.route('/user/bookings', methods=['GET'])
@login_required
def userBookings():
    return 'User Bookings'


@app.route('/user/profile', methods=['POST'])
@login_required
def userProfile():

    new_firstname = request.form.get('firstname')
    new_lastname = request.form.get('lastname')

    user = User.query.get(current_user.id)

    user.firstname = new_firstname
    user.lastname = new_lastname

    db.session.commit()
    flash('Success: Information Updated')
    return redirect('/profile')


@app.route('/user/profile/update-password', methods=['POST'])
@login_required
def updatePassword():

    old_password = request.form.get('current')
    new_password = request.form.get('new')

    user = User.query.get(current_user.id)

    validatePassword = check_password_hash(user.password , old_password)

    if not validatePassword:
        flash('Old Password Incorrect')
        return render_template('pages/user/profile.html')
    
    flash('Password Updated')
    user.password = generate_password_hash(new_password)
    db.session.commit()

    return redirect('/profile')