from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from app import app
from app import db
from app.models import User, PaymentDetails, Membership, Class
from app.models.Package import Package

from app.admin_views import authorize_request, membership_validator


@app.route('/user/classes', methods=['GET'])
@login_required
@membership_validator
def user_classes():

    classes = Class.query.filter_by(category_id = current_user.membership.package.category_id)
    print(current_user.membership.package.category.name)
    # return 'Here'

    if current_user.membership.package.category.name.lower() == 'premium':
        print('Here')
        classes = Class.query.all()
        return render_template('pages/user/classes.html', classes=classes)

    return render_template('pages/user/classes.html', classes=classes)


@app.route('/user/bookings', methods=['GET'])
@login_required
def user_bookings():
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


@app.route('/payment/subscribe/<int:package_id>', methods=['GET', 'POST'])
@login_required
def user_payment_details(package_id):

    package = Package.query.get(package_id)
    
    if request.method == 'POST':

        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number')
        card_cvv = request.form.get('cvv')
        card_expiry_date = datetime.strptime(request.form.get('expiry_date'), "%Y-%m-%d").date()

        if PaymentDetails.query.get(card_number) is not None:
            flash('Account with same number existing')
            return render_template('pages/user/payment-details.html', package=package)

        if any(c.isalpha() for c in card_number):
            flash('Card Number Cannot Container Letters')
            return render_template('pages/user/payment-details.html', package=package)

        if len(card_cvv) > 3 or len(card_cvv) < 3:
            flash('CVV Must Be 3 Characters')
            return render_template('pages/user/payment-details.html', package=package)


        current_date = datetime.now().date()
        if card_expiry_date < current_date:
            flash('Card Expired')
            return render_template('pages/user/payment-details.html', package=package)

        payment_details = PaymentDetails(user_id=current_user.id, card_name=card_name, card_number=card_number, card_expiry_date=card_expiry_date, card_cvv=card_cvv)

        membership = Membership.query.filter_by(user_id=current_user.id).first()
        membership.package_id = package.id

        db.session.add(payment_details)
        db.session.commit()

        flash('Created')
        return redirect(url_for('index'))


    return render_template('pages/user/payment-details.html', package=package)


@app.route('/user/unsubscribe')
@login_required
def unsubscribe_user():

    user = User.query.get(current_user.id)

    user.membership.package = None

    db.session.commit()

    return redirect(url_for('index'))

@app.route('/user/edit/payment-details', methods=['GET', 'POST'])
@login_required
def update_payment_details():

    details = PaymentDetails.query.filter_by(user_id=current_user.id).first()
    print(details.card_name)
    # return('Here')

    if request.method == 'POST':

        card_name = request.form.get('card_name')
        card_number = request.form.get('card_number')
        card_cvv = request.form.get('cvv')
        card_expiry_date = datetime.strptime(request.form.get('expiry_date'), "%Y-%m-%d").date()

        details.card_name = card_name
        details.card_number = card_number
        details.card_cvv = card_cvv
        details.card_expiry_date = card_expiry_date

        if any(c.isalpha() for c in card_number):
            flash('Card Number Cannot Container Letters')
            return render_template('pages/user/update-payment-details.html', details=details)

        if len(card_cvv) > 3 or len(card_cvv) < 3:
            flash('CVV Must Be 3 Characters')
            return render_template('pages/user/update-payment-details.html', details=details)


        current_date = datetime.now().date()
        if card_expiry_date < current_date:
            flash('Card Expired')
            return render_template('pages/user/payment-details.html', details=details)

        db.session.commit()
        flash('Payment Details Updated')
        return redirect(url_for('profile'))

    return render_template('pages/user/update-payment-details.html', details=details)

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
        user.membership.package_id = request.form.get('membership')

        if request.form.get('membership') == None:
            user.membership.package = None

        db.session.commit()
        flash('User Details Updated')

    return render_template('pages/admin/users/edit.html', user=user, memberships=memberships)


@app.route('/user/delete/<int:id>', methods=['GET'])
@login_required
@authorize_request
def delete_user(id):

    user = User.query.get(id)
    user_membership = Membership.query.filter_by(user_id=id).first()
    user_payment_details = PaymentDetails.query.filter_by(user_id=id).first()

    db.session.delete(user)
    db.session.delete(user_membership)
    db.session.delete(user_payment_details)
    db.session.commit()
    flash('User Deleted')

    return redirect(url_for('all_users'))


