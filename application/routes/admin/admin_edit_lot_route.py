from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from flask_security import roles_required
import re
from application.extensions.db_extn import db
from application.helpers.models import ParkingLot, ParkingSpot


admin_edit_lot_route = Blueprint('admin_edit_lot', __name__)


@admin_edit_lot_route.route('/dash/admin/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
@roles_required('admin')
def edit_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    if request.method == 'POST':
        form_data = {
            'location': request.form.get('location', '').strip(),
            'price': request.form.get('price', '').strip(),
            'address': request.form.get('address', '').strip(),
            'pincode': request.form.get('pincode', '').strip(),
            'spots': request.form.get('spots', '').strip()
        }

        if not form_data['location']:
            flash('Location is required.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_edit_lot.edit_lot', lot_id=lot.id))

        if not form_data['address']:
            flash('Address is required.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_edit_lot.edit_lot', lot_id=lot.id))

        if not re.fullmatch(r'\d{6}', form_data['pincode']):
            flash('Pincode must be a 6-digit number.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_edit_lot.edit_lot', lot_id=lot.id))

        try:
            price = float(form_data['price'])
            new_spots = int(form_data['spots'])
            pincode = form_data['pincode']

            if price <= 0:
                flash('Price must be a positive number.', 'danger')
                session['form_data'] = form_data
                return redirect(url_for('admin_edit_lot.edit_lot', lot_id=lot.id))

            if new_spots < 0:
                flash('Number of spots cannot be negative.', 'danger')
                session['form_data'] = form_data
                return redirect(url_for('admin_edit_lot.edit_lot', lot_id=lot.id))

        except ValueError:
            flash('Invalid numeric input for price or number of spots.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_edit_lot.edit_lot', lot_id=lot.id))

        try:
            current_spots = ParkingSpot.query.filter_by(lot_id=lot_id).count()

            lot.prime_location_name = form_data['location']
            lot.price = price
            lot.address = form_data['address']
            lot.pin_code = pincode

            if new_spots > current_spots:
                for _ in range(new_spots - current_spots):
                    db.session.add(ParkingSpot(lot_id=lot.id))

            elif new_spots < current_spots:
                reserved = ParkingSpot.query.filter_by(lot_id =lot.id, status ='O').count()

                if new_spots < reserved:
                    flash(f'Cannot reduce spots below {reserved}', 'danger')
                    session['form_data'] = form_data
                    return redirect(url_for('admin_edit_lot.edit_lot', lot_id=lot.id))

                deletable = ParkingSpot.query.filter_by(lot_id = lot.id, status = 'A').all()

                for spot in deletable[:current_spots - new_spots]:
                    db.session.delete(spot)

            lot.maximum_number_of_spots = new_spots

            db.session.commit()
            session.pop('login_data', None)
            flash('Parking lot updated successfully!', 'success')
            return redirect(url_for('admin_dash.admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_edit_lot.edit_lot', lot_id=lot.id))

    form_data = session.pop('form_data', {})
    return render_template('admin/admin_edit_parking_lot.html', lot=lot, form_data=form_data)
