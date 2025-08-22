from flask import render_template, Blueprint
from flask_security import roles_required, current_user
from application.helpers.models import ReserveParkingSpot
import json


user_history_route = Blueprint('user_history', __name__)


@user_history_route.route('/dash/user/history')
@roles_required('user')
def history():
    reservations = ReserveParkingSpot.query.filter_by(user_id=current_user.id).order_by(ReserveParkingSpot.parking_timestamp.desc()).all()
    completed_reservations = [r for r in reservations if r.leaving_timestamp]
    chart_data = {
        'dates': [r.parking_timestamp.strftime('%Y-%m-%d') for r in completed_reservations],
        'costs': [float(r.total_cost) if r.total_cost else 0 for r in completed_reservations],
        'durations': [float(r.duration_hours) if r.duration_hours else 0 for r in completed_reservations]
    }

    return render_template('user/user_history.html', reservations=reservations, chart_data=json.dumps(chart_data))
