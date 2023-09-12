from flask import redirect, render_template, request, url_for
from app import app
from app import db
from flask_login import login_required, current_user


from app.models.Package import Package, Category, PackageType


@app.route('/admin/dashboard')
@login_required
def admin():
    if not current_user.isAdmin:
       return redirect('/')
    return render_template('pages/admin/dashboard.html')


@app.route('/admin/package/new', methods=['POST', 'GET'])
@login_required
def createPackage():

   categories = Category.query.all()
   package_types = PackageType.query.all()

   if request.method == 'POST':

      package_name = request.form['name']
      package_price = float(request.form['price'])
      package_description = request.form['description']
      package_package_id = int(request.form['package_type'])
      package_category_id = int(request.form['category'])

      package = Package(name=package_name, description=package_description, price=package_price, package_id=package_package_id, category_id=package_category_id)

      db.session.add(package)
      db.session.commit()

      return redirect(url_for('showPackages'))
   return render_template('pages/admin/packages/new.html', categories=categories, package_types=package_types)


@app.route('/admin/packages/')
@login_required
def showPackages():
   packages = Package.query.all()
   return render_template('pages/admin/packages/preview.html', packages=packages)


@app.route('/admin/edit-package/<int:package_id>', methods=['GET', 'POST'])
@login_required
def managePackage(package_id):

   package = Package.query.get(int(package_id))
   categories = Category.query.all()
   package_types = PackageType.query.all()
   
   category = Category.query.get(package.category_id)

   if request.method == 'POST':
      return f'Updating Package {package_id}'
   
   return render_template('pages/admin/packages/edit.html', package=package, categories=categories, package_types=package_types, category=category)