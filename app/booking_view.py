from app import db
from app import app
from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user

from datetime import datetime

from app.admin_views import authorize_request, membership_validator
from app.models.Package import Category
from app.models import Trainer, Class, User

@app.route('/admin/booking/all')
@login_required
@authorize_request
def all_bookings():
    pass


@app.route('/admin/booking/class')
@login_required
@authorize_request
@def class_bookings():
    pass


@app.route('/admin/booking/membership')
@login_required
@authorize_request
@def membership_bookings():
    pass


@app.route('/booking/all')
@login_required
@def user_bookings(class_id):
    pass


@app.route('/booking/class/new/<int:class_id>')
@login_required
@def create_class_booking(class_id):
    pass


@app.route('/booking/membership/new/<int:package_id>')
@login_required
@def create_class_booking(package_id):
    pass