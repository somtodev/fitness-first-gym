from flask import render_template, redirect, session, url_for
from app import app
from flask_login import login_required, current_user

from app.models.Package import Package

# Desc: The Homepage Of Fitness First Gym
@app.route('/')
def index():
    # Fetching all packages
    packages = Package.query.all()

    # Checking if the user is logged in
    if '_user_id' in session:
        # Checking if the user is an admin
        if current_user.isAdmin:
            return redirect(url_for('admin_dashboard'))
        else:
           return render_template('index.html', packages=packages)
    return render_template('index.html', packages=packages)


# Desc: Route for the contact page
@app.route('/contact-us')
def contactUs():
    return render_template('pages/contact.html')


# Desc: Route for the profile page
@app.route('/profile')
@login_required # A Middleware to make sure the user is logged in
def profile():
    return render_template('pages/user/profile.html')
