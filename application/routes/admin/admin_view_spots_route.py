from flask import render_template, Blueprint
from flask_security import roles_required
from application.helpers.models import ParkingLot, ParkingSpot, User, ReserveParkingSpot


admin_view_spots_route = Blueprint('admin_view_spots', __name__)


@admin_view_spots_route.route('/dash/admin/view_spots/<int:lot_id>')
@roles_required('admin')
def view_spots(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()

    spot_details = []
    
    for spot in spots:
        detail = {
            'id': spot.id,
            'status': 'Occupied' if spot.status == 'O' else 'Available',
            'user': None,
            'reservation': None
        }

        if spot.status == 'O':
            reservation = ReserveParkingSpot.query.filter_by(spot_id=spot.id, leaving_timestamp=None).first()

            if reservation:
                user = User.query.get(reservation.user_id)
                detail['user'] = user
                detail['reservation'] = reservation

        spot_details.append(detail)

    return render_template('admin/admin_parking_spot_overview.html', lot=lot, spot_details=spot_details)
