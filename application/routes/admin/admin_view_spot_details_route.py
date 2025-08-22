from flask import render_template, Blueprint, redirect, url_for, flash
from flask_security import roles_required
from datetime import datetime, timedelta, timezone
from application.helpers.models import ParkingSpot, User, ReserveParkingSpot


admin_view_spot_details_route = Blueprint('admin_view_spot_details', __name__)


@admin_view_spot_details_route.route('/dash/admin/spot_details/<int:spot_id>')
@roles_required('admin')
def spot_details(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    reservation = ReserveParkingSpot.query.filter_by(spot_id=spot_id, leaving_timestamp=None).first()

    if not reservation:
        flash('No active reservation found for this spot', 'danger')
        return redirect(url_for('admin_view_spots.view_spots', lot_id=spot.lot_id))

    user = User.query.get(reservation.user_id)
    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    parking_time = reservation.parking_timestamp.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))
    hours_parked = (now - parking_time).total_seconds() / 3600
    estimated_cost = hours_parked * reservation.parking_cost_per_unit_time

    return render_template('admin/admin_single_spot_details.html',spot=spot, reservation=reservation, user=user, hours_parked=hours_parked, estimated_cost=estimated_cost)
