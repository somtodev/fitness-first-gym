from flask import redirect, render_template, request, url_for, flash, session, jsonify
from functools import wraps
from app import app
from app import db
from flask_login import login_required, current_user
from sqlalchemy import inspect, text


from app.models import User, Class, Trainer, MembershipBooking, ClassBooking, Membership
from app.models.Package import Package, Category, PackageType


# Description: A middlware to check if a user is an admin. It's used to protect routes to only admin access.
def authorize_request(view_func):
   @wraps(view_func)
   def wrapped_view(*args, **kwargs):
      
      try:
         if current_user.isAdmin:
               return view_func(*args, **kwargs)
         else:
            flash('Unauthorized')
            return redirect('/')
      except Exception as error:
         # return error
         return render_template('pages/error/500.html', error=error)
         
   return wrapped_view

# Description: A middleware to protect routes from non-membered users
def membership_validator(view_func):
   @wraps(view_func)
   def wrapped_view(*args, **kwargs):
      
      try:
         if current_user.membership.package is None:
             flash('Not A Member')
             return redirect('/')
         else:
            return view_func(*args, **kwargs)
      except Exception as error:
         return render_template('pages/error/500.html', error=error)
         
   return wrapped_view


# Description: Route to admin dashboard
@app.route('/admin/dashboard')
@login_required
@authorize_request
def admin_dashboard():
   if not current_user.isAdmin:
      return redirect('/')

   return render_template('pages/admin/dashboard.html' , data= dict(
      users = len(User.query.all()),
      packages = len(Package.query.all()),
      b_mem = len(MembershipBooking.query.all()),
      b_class = len(ClassBooking.query.all()),
      trainers = len(Trainer.query.all())
   ))



# Description: Route to create a new package
@app.route('/admin/package/new', methods=['POST', 'GET'])
@login_required
@authorize_request
def new_package():

   categories = Category.query.all()
   package_types = PackageType.query.all()

   if request.method == 'POST':

      package_name = request.form.get('name')

      matching_package = Package.query.filter_by(name=package_name).first()
      
      if matching_package:
         flash('Info: Package With Same Name Exists')
         return render_template('pages/admin/packages/new.html', categories=categories, package_types=package_types)
         
      package_price = float(request.form.get('price'))
      package_description = request.form.get('description')
      package_package_id = int(request.form.get('package_type'))
      package_category_id = int(request.form.get('category'))

      package = Package(name=package_name, description=package_description, price=package_price, package_id=package_package_id, category_id=package_category_id)
      db.session.add(package)
      db.session.commit()

      return redirect(url_for('all_packages'))
      
   return render_template('pages/admin/packages/new.html', categories=categories, package_types=package_types)


@app.route('/admin/package/all')
@login_required
@authorize_request
def all_packages():
   packages = Package.query.all()
   return render_template('pages/admin/packages/preview.html', packages=packages)


@app.route('/admin/package/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@authorize_request
def edit_package(id):

   package = Package.query.get(int(id))
   categories = Category.query.all()
   package_types = PackageType.query.all()
   
   category = Category.query.get(package.category_id)

   if request.method == 'POST':

      found_package_name = Package.query.filter_by(name=request.form['name'])

      print(found_package_name)

      if 'name' in found_package_name:
         flash('Package With Same Name Exists')

      package.name = request.form.get('name')
      package.price = request.form.get('price')
      package.description = request.form.get('description')
      package.package_id = int(request.form.get('package_type'))
      package.category_id = int(request.form.get('category'))

      db.session.commit()
      return redirect(url_for('all_packages'))
      
   
   return render_template('pages/admin/packages/edit.html', package=package, categories=categories, package_types=package_types)


@app.route('/admin/package/delete/<int:id>', methods=['GET'])
@login_required
@authorize_request
def delete_package(id):
   
   package = Package.query.get(id)

   db.session.delete(package)
   db.session.commit()

   flash('Successfully Deleted')
   return redirect('/admin/package/all')


@app.route('/admin/categories', methods=['GET'])
@login_required
@authorize_request
def manage_categories():
   categories = Category.query.all()
   return render_template('pages/admin/category.html', categories=categories)


@app.route('/admin/category/new', methods=['POST'])
@login_required
@authorize_request
def new_category():
   content = request.form.get('name')

   category = Category(name=content)

   db.session.add(category)
   db.session.commit()

   return redirect(url_for('manage_categories'))


@app.route('/admin/category/edit/<int:id>', methods=['POST'])
@login_required
@authorize_request
def edit_category(id):

   category = Category.query.get(id)

   print(category.name)

   category.name = request.form.get('name')
   db.session.commit()

   flash('Category Updated')

   return redirect(url_for('manage_categories'))

@app.route('/admin/category/delete/<int:id>', methods=['GET'])
@login_required
@authorize_request
def delete_category(id):

    # CLASS, TRAINER, PACKAGE

   category = Category.query.get(id)

   if category is None:
       return jsonify({'message': 'Parent Not Found'}), 404

   cate_class = Class.query.filter_by(category_id=id).all()
   cate_trainer = Trainer.query.filter_by(category_id=id).all()
   cate_package = Package.query.filter_by(category_id=id).all() 

   for _class in cate_class:
       db.session.delete(_class)
       flash(f'All {category.name} classes deleted')
   for trainer in cate_trainer:
       db.session.delete(trainer)
       flash(f'All {category.name} packages deleted')
   for package in cate_package:
       flash(f'All {category.name} trainers deleted')
       db.session.delete(package)

   db.session.delete(category)
   flash('Category Deleted')   

   db.session.commit()

   return redirect(url_for('manage_categories'))
