from app import db
from app import app
from flask import redirect, render_template, flash, url_for
from flask_login import login_required, current_user

from app.admin_views import authorize_request, membership_validator
from app.models import ClassBooking , MembershipBooking


@app.route('/admin/booking/classes')
@login_required
@authorize_request
def class_bookings():
    bookings = ClassBooking.query.all()
    return render_template('pages/admin/booking/classes.html', bookings=bookings)


@app.route('/admin/booking/memberships')
@login_required
@authorize_request
def membership_bookings():
    bookings = MembershipBooking.query.all()
    return render_template('pages/admin/booking/memberships.html', bookings=bookings)


@app.route('/booking/class/new/<int:class_id>')
@login_required
@membership_validator
def create_class_booking(class_id):

    found_booking = ClassBooking.query.filter_by(class_id=class_id).first()

    if found_booking is not None:
        flash('Class Already Booked')
        return redirect(url_for('user_classes'))

    booking = ClassBooking(user_id=current_user.id, class_id=class_id)

    db.session.add(booking)
    db.session.commit()

    bookings = ClassBooking.query.filter_by(user_id=current_user.id)

    return render_template('pages/user/booking-details.html',
                           bookings=bookings)



@app.route('/booking/delete/class/<int:id>')
@login_required
@authorize_request
def delete_class_booking(id):
    
    booking = ClassBooking.query.get(id)

    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('class_bookings'))

 
@app.route('/booking/remove/<int:booking_id>')
@login_required
@membership_validator
def cancel_booking(booking_id):

    booking = ClassBooking.query.filter_by(id=booking_id, user_id=current_user.id).first()

    db.session.delete(booking)
    db.session.commit()

    return redirect(url_for('user_bookings'))
