from flask import render_template, redirect, session
from app import app
from flask_login import login_required, current_user


@app.route('/')
def index():
    if 'user' in session:
        if current_user.isAdmin:
            return redirect('/admin/dashboard')
    return render_template('index.html')


@app.route('/contact-us')
def contactUs():
    return render_template('pages/contact.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('pages/user/profile.html')
