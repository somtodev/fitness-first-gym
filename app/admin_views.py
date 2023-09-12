from flask import redirect, render_template
from app import app
from flask_login import login_required, current_user


@app.route('/admin/dashboard')
@login_required
def admin():
    if not current_user.isAdmin:
       return redirect('/')
    return render_template('pages/admin/dashboard.html')
