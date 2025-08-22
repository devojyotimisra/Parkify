from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from flask_security import roles_required
import re
from application.extensions.db_extn import db
from application.helpers.models import ParkingLot, ParkingSpot


admin_add_lot_route = Blueprint('admin_add_lot', __name__)


@admin_add_lot_route.route('/dash/admin/add_lot', methods=['GET', 'POST'])
@roles_required('admin')
def add_lot():
    if request.method == 'POST':
        form_data = {
            'location': request.form.get('location', '').strip(),
            'address': request.form.get('address', '').strip(),
            'pincode': request.form.get('pincode', '').strip()
        }
        raw_price = request.form.get('price', '').strip()
        raw_spots = request.form.get('spots', '').strip()

        if not form_data['location']:
            flash('Location is required.', 'danger')
            session['lot_form'] = form_data | {'price': raw_price, 'spots': raw_spots}
            return redirect(url_for('admin_add_lot.add_lot'))

        if not form_data['address']:
            flash('Address is required.', 'danger')
            session['lot_form'] = form_data | {'price': raw_price, 'spots': raw_spots}
            return redirect(url_for('admin_add_lot.add_lot'))

        if not re.fullmatch(r'\d{6}', form_data['pincode']):
            flash('Pincode must be a 6-digit number.', 'danger')
            session['lot_form'] = form_data | {'price': raw_price, 'spots': raw_spots}
            return redirect(url_for('admin_add_lot.add_lot'))

        try:
            price = float(raw_price)
            if price < 0:
                raise ValueError
        except ValueError:
            flash('Invalid price. Must be a positive number.', 'danger')
            session['lot_form'] = form_data | {'price': raw_price, 'spots': raw_spots}
            return redirect(url_for('admin_add_lot.add_lot'))

        try:
            spots = int(raw_spots)
            if spots <= 0:
                raise ValueError
        except ValueError:
            flash('Number of spots must be a positive integer.', 'danger')
            session['lot_form'] = form_data | {'price': raw_price, 'spots': raw_spots}
            return redirect(url_for('admin_add_lot.add_lot'))

        new_lot = ParkingLot(
            prime_location_name=form_data['location'],
            price=price,
            address=form_data['address'],
            pin_code=form_data['pincode'],
            maximum_number_of_spots=spots
        )
        db.session.add(new_lot)
        db.session.commit()

        for _ in range(spots):
            spot = ParkingSpot(lot_id=new_lot.id)
            db.session.add(spot)
        db.session.commit()

        flash('Parking lot added successfully!', 'success')
        return redirect(url_for('admin_dash.admin_dashboard'))

    form_data = session.pop('lot_form', {})
    return render_template('admin/admin_add_parking_lot.html', form_data=form_data)
