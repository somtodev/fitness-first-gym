from flask import render_template, redirect, session, url_for
from app import app
from flask_login import login_required, current_user

from app.models.Package import Package


@app.route('/')
def index():
    packages = Package.query.all()
    if '_user_id' in session:
        if current_user.isAdmin:
            return redirect(url_for('admin_dashboard'))
        else:
           return render_template('index.html', packages=packages)
    return render_template('index.html', packages=packages)


@app.route('/contact-us')
def contactUs():
    return render_template('pages/contact.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('pages/user/profile.html')
