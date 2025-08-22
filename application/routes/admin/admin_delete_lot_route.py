from flask import Blueprint, redirect, url_for, flash
from flask_security import roles_required
from application.extensions.db_extn import db
from application.helpers.models import ParkingLot, ParkingSpot


admin_delete_lot_route = Blueprint('admin_delete_lot', __name__)


@admin_delete_lot_route.route('/dash/admin/delete_lot/<int:lot_id>', methods=['POST'])
@roles_required('admin')
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='O').count()
    if occupied_spots > 0:
        flash('Cannot delete parking lot with occupied spots', 'danger')
        return redirect(url_for('admin_dash.admin_dashboard'))

    ParkingSpot.query.filter_by(lot_id=lot_id).delete()
    
    db.session.delete(lot)
    db.session.commit()

    flash('Parking lot deleted successfully!', 'success')
    return redirect(url_for('admin_dash.admin_dashboard'))
