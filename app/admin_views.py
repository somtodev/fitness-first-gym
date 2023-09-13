from flask import redirect, render_template, request, url_for, flash, session
from functools import wraps
from app import app
from app import db
from flask_login import login_required, current_user


from app.models.Package import Package, Category, PackageType
from app.models import User

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


@app.route('/admin/dashboard')
@login_required
@authorize_request
def admin_dashboard():
   if not current_user.isAdmin:
      return redirect('/')
   return render_template('pages/admin/dashboard.html')



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