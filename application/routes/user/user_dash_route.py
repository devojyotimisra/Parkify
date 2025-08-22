from flask import render_template, Blueprint
from flask_security import roles_required, current_user
from application.helpers.models import ParkingLot, ReserveParkingSpot


user_dash_route = Blueprint('user_dash', __name__)


@user_dash_route.route('/dash/user')
@roles_required('user')
def user_dashboard():
    active_reservation = ReserveParkingSpot.query.filter_by(user_id=current_user.id, leaving_timestamp=None).order_by(ReserveParkingSpot.parking_timestamp.desc()).all()
    parking_lots = ParkingLot.query.order_by(ParkingLot.prime_location_name.asc()).all()
    available_lots = [lot for lot in parking_lots if lot.available_spots_count > 0]

    return render_template('user/user_dashboard.html', active_reservation=active_reservation, available_lots=available_lots, user=current_user)
