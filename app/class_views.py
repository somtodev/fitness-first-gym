from app import app
from flask import request, redirect, render_template, flash
from flask_login import login_required, current_user, login_user
from app import db
from app.models import User
from app.models.Package import Package
from werkzeug.security import generate_password_hash, check_password_hash

from app.admin_views import authorize_request


@app.route('/admin/class/all')
@login_required
def all_classes():
    return 'All Classes'


@app.route('/admin/class/new', methods=['GET','POST'])
@login_required
@authorize_request
def create_class():
    return 'New Class'


@app.route('/class/<int:user_id>/', methods=['GET'])
@login_required
def get_user_class():
    pass