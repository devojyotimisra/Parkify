from flask import render_template, Blueprint
from flask_security import roles_required
import json
from application.helpers.models import ReserveParkingSpot, ParkingLot


admin_history_route = Blueprint('admin_history', __name__)


@admin_history_route.route('/dash/admin/history')
@roles_required('admin')
def history():
    reservations = ReserveParkingSpot.query.order_by(ReserveParkingSpot.leaving_timestamp.desc()).all()
    lots = ParkingLot.query.all()

    lot_revenue = {}
    lot_occupancy = {}

    for lot in lots:
        lot_occupancy[lot.prime_location_name] = {"total": lot.maximum_number_of_spots, "occupied": 0}

    for res in reservations:
        if res.spot is None and ParkingLot.query.filter(ParkingLot.id == res.lot_id).first() != None:
            lot_name = ParkingLot.query.filter(ParkingLot.id == res.lot_id).first().prime_location_name

        elif res.spot is None:
            lot_name = f'Deleted(LotID: {res.lot_id})'

        else:
            lot_name = res.spot.lot.prime_location_name

        if res.leaving_timestamp is not None:
            lot_revenue[lot_name] = lot_revenue.get(lot_name, 0) + (res.total_cost or 0)

        if not lot_name.startswith('Deleted') and res.leaving_timestamp is None:
            lot_occupancy[lot_name]["occupied"] += 1

    chart_data = {
        "revenue": {"labels": list(lot_revenue.keys()), "data": list(lot_revenue.values())},
        "occupancy": {"labels": list(lot_occupancy.keys()), "available": [lot_occupancy[lot]["total"] - lot_occupancy[lot]["occupied"] for lot in lot_occupancy], "occupied": [lot_occupancy[lot]["occupied"] for lot in lot_occupancy]}
    }

    return render_template('admin/admin_history.html', reservations=list(reversed(reservations)), chart_data=json.dumps(chart_data))
