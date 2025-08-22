from flask import Blueprint, request, redirect, url_for, flash
from flask_security import roles_required, current_user
from datetime import datetime, timedelta, timezone
import re
from application.extensions.db_extn import db
from application.helpers.models import ParkingLot, ParkingSpot, ReserveParkingSpot


user_book_slot_route = Blueprint('user_book_slot', __name__)


@user_book_slot_route.route('/dash/user/book_slot/<int:lot_id>', methods=['POST'])
@roles_required('user')
def book_slot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spot_id = request.form.get('spot_id')
    vehicle_number = request.form.get('vehicle_number', '').strip().upper()

    if not spot_id:
        flash('Please select a parking space', 'danger')
        return redirect(url_for('user_select_slot.select_slot', lot_id=lot_id))

    if not re.fullmatch(r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$', vehicle_number):
        flash('Invalid vehicle number format. Example: DL01AB1234', 'danger')
        return redirect(url_for('user_select_slot.select_slot', lot_id=lot_id))

    if ReserveParkingSpot.query.filter(ReserveParkingSpot.vehicle_number == vehicle_number, ReserveParkingSpot.leaving_timestamp == None).first():
        flash('This vehicle is already parked in another spot.', 'danger')
        return redirect(url_for('user_select_slot.select_slot', lot_id=lot_id))

    spot = ParkingSpot.query.get_or_404(spot_id)

    if spot.lot_id != lot_id:
        flash('Invalid parking space selected', 'danger')
        return redirect(url_for('user_select_slot.select_slot', lot_id=lot_id))

    if spot.status != 'A':
        flash('This parking space is already occupied', 'danger')
        return redirect(url_for('user_select_slot.select_slot', lot_id=lot_id))

    reservation = ReserveParkingSpot(
        lot_id=spot.lot_id,
        spot_id=spot.id,
        user_id=current_user.id,
        vehicle_number=vehicle_number,
        parking_cost_per_unit_time=lot.price,
        parking_timestamp=datetime.now(timezone(timedelta(hours=5, minutes=30))),
    )

    spot.status = 'O'

    db.session.add(reservation)
    db.session.commit()

    flash('Parking spot booked successfully!', 'success')
    return redirect(url_for('user_dash.user_dashboard'))
