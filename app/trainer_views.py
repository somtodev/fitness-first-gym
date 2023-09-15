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
    return render_template('pages/admin/trainer/preview.html')
    


@app.route('/admin/trainer/new', methods=['GET','POST'])
@login_required
@authorize_request
def new_trainer():
    
    if request.form == 'POST':
        pass

    return render_template('pages/admin/trainer/new.html')


@app.route('/admin/trainer/edit/<int:id>', methods=['GET','POST'])
@login_required
@authorize_request
def edit_trainer(id):
    return render_template('pages/admin/trainer/edit.html')
    


@app.route('/admin/trainer/delete/<int:id>')
@login_required
@authorize_request
def delete_trainer(id):
    pass