from flask import render_template, Blueprint, flash, session
from flask_security import roles_required
from datetime import datetime, timedelta, timezone
from application.helpers.models import ParkingLot, ParkingSpot


user_select_slot_route = Blueprint('user_select_slot', __name__)


@user_select_slot_route.route('/dash/user/select_slot/<int:lot_id>', methods=['GET'])
@roles_required('user')
def select_slot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()

    if '_flashes' not in session:
        flash(f"You are selecting a parking space at <strong>{lot.prime_location_name}</strong>.<br> Price: ₹{lot.price:.2f} per hour.<br> Available spaces: {lot.available_spots_count}", 'info')

    return render_template('user/user_select_parking_space.html', lot=lot, spots=spots, now=datetime.now(timezone(timedelta(hours=5, minutes=30))))
