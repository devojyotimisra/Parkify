from flask import render_template, request, Blueprint
from flask_security import roles_required
from application.helpers.models import ParkingLot, ParkingSpot, User, ReserveParkingSpot


admin_search_route = Blueprint('admin_search', __name__)


@admin_search_route.route('/dash/admin/search')
@roles_required('admin')
def search():
    query = request.args.get('query', '')
    type = request.args.get('type', 'lot')

    results = []
    
    if query:
        if type == 'lot':
            results = ParkingLot.query.filter(ParkingLot.prime_location_name.contains(query)).all()

        elif type == 'user':
            results = User.query.filter(User.name.contains(query) | User.email.contains(query)).all()

        elif type == 'vehicle':
            reservations = ReserveParkingSpot.query.filter(ReserveParkingSpot.vehicle_number.contains(query)).all()
            results = [(res, User.query.get(res.user_id), ParkingSpot.query.get(res.spot_id)) for res in reservations]

    return render_template('admin/admin_search_results.html', results=results, query=query, type=type)
