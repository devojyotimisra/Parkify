from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from werkzeug.security import generate_password_hash
from flask_security import login_user
import re
from application.extensions.db_extn import db
from application.helpers.models import User, Role


signup_route = Blueprint('signup', __name__)


@signup_route.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form_data = {
            'email': request.form.get('email', '').strip(),
            'name': request.form.get('name', '').strip(),
            'address': request.form.get('address', '').strip(),
            'pincode': request.form.get('pincode', '').strip(),
            'vehicle_number': request.form.get('vehicle_number', '').strip().upper(),
        }
        
        raw_password = request.form.get('password', '').strip()
        raw_confirm_password = request.form.get('confirm_password', '').strip()

        if not form_data['email'] or not re.match(r'^[^@ \t\r\n]+@[^@ \t\r\n]+$', form_data['email']):
            flash('Invalid email address.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('signup.signup'))

        if not raw_password or len(raw_password) < 5:
            flash('Password must be at least 5 characters long.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('signup.signup'))
        
        if raw_confirm_password != raw_password:
            flash('Password and Confrim Password Dont Match', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('signup.signup'))

        if not form_data['name']:
            flash('Full name is required.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('signup.signup'))

        if not form_data['address']:
            flash('Address is required.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('signup.signup'))

        if not re.fullmatch(r'\d{6}', form_data['pincode']):
            flash('Pincode must be a 6-digit number.', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('signup.signup'))

        if form_data['vehicle_number'] and not re.fullmatch(r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$', form_data['vehicle_number']):
            flash('Invalid vehicle number format. Example: DL01AB1234', 'danger')
            session['form_data'] = form_data
            return redirect(url_for('signup.signup'))

        if User.query.filter_by(email=form_data['email']).first():
            flash('Email already exists! Please login instead.', 'danger')
            return redirect(url_for('login.login'))

        new_user = User(
            email=form_data['email'],
            password=generate_password_hash(raw_password),
            name=form_data['name'],
            address=form_data['address'],
            pincode=form_data['pincode'],
            vehicle_number=form_data['vehicle_number'],
            active=True
        )
        user_role = Role.query.filter_by(name='user').first()
        new_user.roles.append(user_role)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        session.pop('login_data', None)
        flash('Sign Up successful!', 'success')
        return redirect(url_for('user_dash.user_dashboard'))

    form_data = session.pop('form_data', {})
    return render_template('general/signup.html', form_data=form_data)
