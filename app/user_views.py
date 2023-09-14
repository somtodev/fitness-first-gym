from app import app
from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user, login_user
from app import db
from app.models import User
from app.models.Package import Package
from werkzeug.security import generate_password_hash, check_password_hash

from app.admin_views import authorize_request


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
def user_profile():

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
def update_password():

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


@app.route('/users/all')
@login_required
@authorize_request
def all_users():
   users = User.query.all()
   return render_template('pages/admin/users/preview.html', users=users)


@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@authorize_request
def modify_user(id):

    user = User.query.get(id)
    memberships = Package.query.all()
    
    if request.method == 'POST':
        user.firstname = request.form.get('firstname')
        user.lastname = request.form.get('lastname')
        user.email = request.form.get('email')
        user.membership_id = request.form.get('membership')

        db.session.commit()
        flash('User Details Updated')

    return render_template('pages/admin/users/edit.html', user=user, memberships=memberships)


@app.route('/user/delete/<int:id>', methods=['GET'])
@login_required
@authorize_request
def delete_user(id):

    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()
    flash('User Deleted')

    return redirect(url_for('all_users'))