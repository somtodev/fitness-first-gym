from flask import render_template, request, redirect, session, url_for, flash
from app import app
from app import db
from app.models import User, Membership
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/auth/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        user_email = request.form['email']
        user_password = request.form['password']

        user = User.query.filter_by(email=user_email).first()
        if not user:
            flash('No Account Associated With Email')
            return render_template('pages/auth/login.html')
        hashedPassword= user.password
        validatePassword = check_password_hash(hashedPassword, user_password)

        if not validatePassword: 
            flash('Incorrect Password')
            return render_template('pages/auth/login.html')
        else:
            login_user(user)
            if not user.isAdmin:
                flash(f'Success: Welcome, {current_user.firstname}')
                return redirect(url_for('index'))
            else:
                return redirect('/admin/dashboard')

    else:
        return render_template('pages/auth/login.html')


@app.route('/auth/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

        user_fn = request.form['firstname']
        user_ln = request.form['lastname']
        user_email = request.form['email']
        user_password = generate_password_hash(request.form['password'])
        print(user_password)

        existing_user = User.query.filter_by(email=user_email).first()
        print(existing_user)

        if existing_user is not None:
            flash("Another Account Uses That Mail Address")
            return render_template('pages/auth/register.html')

        user = User(firstname=user_fn, lastname=user_ln, email=user_email, password=user_password)

        try:
            db.session.add(user)
            user = User.query.filter_by(email=user_email).first()
            membership = Membership(user_id=user.id)
            db.session.add(membership)
            db.session.commit()
            return redirect('/auth/login')
        except Exception as err:
            print(err)
            flash('Error')
            return render_template('pages/auth/register.html',) 
    else:
        return render_template('pages/auth/register.html')


@app.route('/auth/logout')
def logout():
    logout_user()
    flash('Logged Out')
    return redirect(url_for('index'))
