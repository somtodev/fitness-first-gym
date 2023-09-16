from app import db
from app import app

from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user

from app.admin_views import authorize_request
from app.models.Package import Category
from app.models import Trainer, Class


@app.route('/admin/trainer/all', methods=['GET'])
@login_required
@authorize_request
def all_trainers():

    trainers = Trainer.query.all()

    if trainers is None:
        flash('No Trainers Available')
        return redirect(url_for('all_trainers'))

    return render_template('pages/admin/trainer/preview.html', trainers=trainers)
    


@app.route('/admin/trainer/new', methods=['GET','POST'])
@login_required
@authorize_request
def new_trainer():

    categories = Category.query.all()
    
    if request.method == 'POST':

        
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        category = int(request.form.get('category'))

        trainer = Trainer(firstname=firstname, lastname=lastname, category_id=category)
        print(trainer)

        db.session.add(trainer)
        db.session.commit()

        flash('Trainer Created')
        return redirect(url_for('all_trainers'))


    return render_template('pages/admin/trainer/new.html', categories=categories)


@app.route('/admin/trainer/edit/<int:id>', methods=['GET','POST'])
@login_required
@authorize_request
def edit_trainer(id):

    trainer = Trainer.query.get(id)
    categories = Category.query.all()

    if trainer is None:
        flash(f'No Trainer With ID({id})')
        return redirect(url_for('all_trainers'))

    if request.method == 'POST':

        trainer.firstname = request.form.get('firstname')
        trainer.lastname = request.form.get('lastname')
        trainer.category_id = request.form.get('category')

        db.session.commit()
        flash('Train Details Updated')
        return redirect(url_for('all_trainers'))
    

    return render_template('pages/admin/trainer/edit.html', trainer=trainer, categories=categories)
    


@app.route('/admin/trainer/delete/<int:id>')
@login_required
@authorize_request
def delete_trainer(id):
    trainer = Trainer.query.get(id)

    if trainer is None:
        flash('Cannot Delete Non-Existing Trainer')
        return redirect(url_for('all_trainers'))

    db.session.delete(trainer)
    db.session.commit()
    return redirect(url_for('all_trainers'))