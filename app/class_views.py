from app import app
from flask import request, redirect, render_template, flash
from flask_login import login_required, current_user
from app import db

from app.admin_views import authorize_request

@app.route('/admin/class/all')
@login_required
def all_classes():
    return render_template('pages/admin/class/preview.html')


@app.route('/admin/class/new', methods=['GET','POST'])
@login_required
@authorize_request
def create_class():
    if request.method == 'POST':
        return 'Creating Class'
    return render_template('pages/admin/class/new.html')


@app.route('/class/<int:user_id>/', methods=['GET'])
@login_required
def get_user_class(user_id):
    pass