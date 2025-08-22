from flask import render_template, Blueprint
from flask_security import roles_required, current_user
from application.helpers.models import ParkingLot


admin_dash_route = Blueprint('admin_dash', __name__)


@admin_dash_route.route('/dash/admin')
@roles_required('admin')
def admin_dashboard():
    parking_lots = ParkingLot.query.all()
    return render_template('admin/admin_dashboard.html', parking_lots=parking_lots, user=current_user)
