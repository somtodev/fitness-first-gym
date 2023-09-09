from app import app
from flask import request, redirect, render_template


@app.route('/user')
def user():
    return 'User'

@app.route('/user/profile', methods=['POST', 'GET'])
def userProfile():
    if request.method == 'POST':
        pass
    else:
        return 'User Profile'