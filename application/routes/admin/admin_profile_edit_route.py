from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from flask_security import roles_required, current_user
import re
from werkzeug.security import generate_password_hash
from application.extensions.db_extn import db


admin_profile_edit_route = Blueprint('admin_profile_edit', __name__)


@admin_profile_edit_route.route('/dash/admin/edit_profile', methods=['GET', 'POST'])
@roles_required('admin')
def edit_profile():
    if request.method == 'POST':
        form_data = {
            'email': request.form.get('email', '').strip(),
            'name': request.form.get('name', '').strip(),
            'address': request.form.get('address', '').strip(),
            'pincode': request.form.get('pincode', '').strip()
        }
        raw_password = request.form.get('password', '').strip()
        raw_confirm_password = request.form.get('confirm_password', '').strip()

        if not form_data['email'] or not re.match(r'^[^@ \t\r\n]+@[^@ \t\r\n]+$', form_data['email']):
            flash('Invalid email address.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_profile_edit.edit_profile'))

        if not form_data['name']:
            flash('Full name is required.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_profile_edit.edit_profile'))

        if not form_data['address']:
            flash('Address is required.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_profile_edit.edit_profile'))

        if not re.fullmatch(r'\d{6}', form_data['pincode']):
            flash('Pincode must be a 6-digit number.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_profile_edit.edit_profile'))

        if raw_password and len(raw_password) < 5:
            flash('Password must be at least 5 characters long.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_profile_edit.edit_profile'))

        if raw_confirm_password != raw_password:
            flash('Password and Confrim Password Dont Match', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('admin_profile_edit.edit_profile'))

        current_user.email = form_data['email']
        current_user.name = form_data['name']
        current_user.address = form_data['address']
        current_user.pincode = form_data['pincode']
        current_user.password = generate_password_hash(raw_password)

        db.session.commit()
        session.pop('login_data', None)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin_profile.profile'))

    form_data = session.pop('form_data', None)
    return render_template('admin/admin_edit_profile.html', form_data=form_data)
