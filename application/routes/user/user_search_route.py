from flask import render_template, Blueprint, request
from flask_security import roles_required
from application.helpers.models import ParkingLot


user_search_route = Blueprint('user_search', __name__)


@user_search_route.route('/dash/user/search')
@roles_required('user')
def search():
    location = request.args.get('location', '')
    query = ParkingLot.query

    if location:
        query = query.filter(ParkingLot.prime_location_name.contains(location) | ParkingLot.address.contains(location))

    parking_lots = query.all()
    available_lots = [lot for lot in parking_lots if lot.available_spots_count > 0]

    return render_template('user/user_search_parking.html', available_lots=available_lots, location=location)
