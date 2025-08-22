from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_security import roles_required, current_user
from datetime import datetime, timedelta, timezone
from application.extensions.db_extn import db
from application.helpers.models import ParkingLot, ParkingSpot, ReserveParkingSpot


user_release_slot_route = Blueprint('user_release_slot', __name__)


@user_release_slot_route.route('/dash/user/release_slot/<int:reservation_id>', methods=['GET', 'POST'])
@roles_required('user')
def release_spot(reservation_id):
    reservation = ReserveParkingSpot.query.get_or_404(reservation_id)

    if reservation.user_id != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('user_dash.user_dashboard'))

    if reservation.leaving_timestamp:
        flash('This reservation is already completed', 'danger')
        return redirect(url_for('user_dash.user_dashboard'))

    spot = ParkingSpot.query.get(reservation.spot_id)

    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    parking_time = reservation.parking_timestamp.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))

    duration_seconds = (now - parking_time).total_seconds()
    duration_hours = duration_seconds / 3600
    total_cost = duration_hours * reservation.parking_cost_per_unit_time

    if request.method == 'POST':
        reservation.leaving_timestamp = now
        reservation.duration_hours = duration_hours
        reservation.total_cost = total_cost
        spot.status = 'A'

        db.session.commit()

        flash('Parking spot released successfully!', 'success')
        return redirect(url_for('user_history.history'))

    lot = ParkingLot.query.get(spot.lot_id)

    flash(f"Spot ID: <strong>#{spot.id}</strong> at <strong>{lot.prime_location_name}</strong>",'info')
    return render_template('user/user_release_spot.html', reservation=reservation, duration_hours=duration_hours, total_cost=total_cost, now=now)
