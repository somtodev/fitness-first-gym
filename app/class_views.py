from app import db
from app import app
from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user

from datetime import datetime

from app.admin_views import authorize_request
from app.models.Package import Category
from app.models import Trainer, Class


@app.route('/admin/class/all')
@login_required
def all_classes():
    classes = Class.query.all()
    return render_template('pages/admin/class/preview.html', classes=classes)


@app.route('/admin/class/new', methods=['GET','POST'])
@login_required
@authorize_request
def create_class():

    categories = Category.query.all()
    trainers = Trainer.query.all()

    if request.method == 'POST':

        class_name = request.form.get('name')
        class_description = request.form.get('description')
        class_schedule = datetime.strptime(request.form.get('schedule'), '%Y-%m-%dT%H:%M')
        class_capacity = request.form.get('capacity')
        class_trainer = request.form.get('trainer')
        class_category = request.form.get('category')


        new_class = Class(name=class_name, description=class_description, schedule=class_schedule, trainer_id=class_trainer, category_id=class_category, max_capacity=class_capacity)
        
        try:
            db.session.add(new_class)
            db.session.commit()
        except Exception as error:
            print(error)

        flash('Class Created')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('pages/admin/class/new.html', categories=categories, trainers=trainers)


@app.route('/admin/class/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@authorize_request
def edit_class(id):

    found_class = Class.query.get(id)
    
    categories = Category.query.all()
    trainers = Trainer.query.all()

    if request.method == 'POST':

        found_class.name = request.form.get('name')
        found_class.description = request.form.get('description')
        found_class.schedule = datetime.strptime(request.form.get('schedule'), '%Y-%m-%dT%H:%M')
        found_class.max_capacity = request.form.get('capacity')
        found_class.trainer_id = request.form.get('trainer')
        found_class.category_id = request.form.get('category')

        try:
            db.session.commit()
            flash('Class Updated')
            return redirect(url_for('all_classes'))
        except Exception as error:
            print(error)
            flash('')

    return render_template('pages/admin/class/edit.html', _class=found_class, categories=categories, trainers=trainers)


@app.route('/admin/class/delete/<int:id>')
@login_required
@authorize_request
def delete_class(id):

    found_class = Class.query.get(id)

    try:
        db.session.delete(found_class)
        flash('Class Deleted')
        db.session.commit()
    except Exception as excep:
        print(excep)
        flash('Class Not Deleted')

    return redirect(url_for('all_classes'))


@app.route('/class/<int:user_id>/', methods=['GET'])
@login_required
def get_user_class(user_id):
    pass