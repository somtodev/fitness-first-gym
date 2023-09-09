from flask import render_template, request, redirect
from app import app
from app import db
from app.models import User


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact-us')
def contactUs():
    return render_template('pages/contact.html')


@app.route('/auth/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        user_email = request.form['email']
        user_password = request.form['password']

        # return redirect('/')
        return user_email + user_password
    else:
        return render_template('pages/auth/login.html')
        pass


@app.route('/auth/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

        user_fn = request.form['firstname']
        user_ln = request.form['lastname']
        user_email = request.form['email']
        user_password = request.form['password']

        existing_user = db.session.query(User.id).filter_by(email=user_email).first()

        if existing_user:
            return render_template('pages/auth/register.html', msg="Another Account Uses That Mail Address")

        user = User(firstname=user_fn, lastname=user_ln, email=user_email, password=user_password)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/auth/login')
        except Exception as err:
            print(err)
            return render_template('pages/auth/register.html', msg='Error') 
    else:
        return render_template('pages/auth/register.html')
        pass
