from app import db
from app import app

from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user

from app.admin_views import authorize_request
from app.models.Package import Category
from app.models import Trainer, Class


@app.route('/admin/trainer/all')
@login_required
@authorize_request
def all_trainers():
    pass


@app.route('/admin/trainer/new')
@login_required
@authorize_request
def edit_trainer():
    pass


@app.route('/admin/trainer/edit/<int:id>')
@login_required
@authorize_request
def edit_trainer(id):
    pass


@app.route('/admin/trainer/delete/<int:id>')
@login_required
@authorize_request
def delete_trainer(id):
    pass