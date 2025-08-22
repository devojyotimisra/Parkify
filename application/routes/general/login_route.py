from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from werkzeug.security import check_password_hash
from flask_security import login_user
import re
from application.helpers.models import User


login_route = Blueprint('login', __name__)


@login_route.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = {'email': request.form.get('email', '').strip()}
        
        raw_password = request.form.get('password', '').strip()

        if not form_data['email'] or not re.match(r'^[^@ \t\r\n]+@[^@ \t\r\n]+$', form_data['email']):
            flash('Invalid email address.', 'danger')
            session['login_data'] = form_data
            return redirect(url_for('login.login'))

        if not raw_password or len(raw_password) < 5:
            flash('Password must be at least 5 characters long.', 'danger')
            session['login_data'] = form_data
            return redirect(url_for('login.login'))

        user = User.query.filter_by(email=form_data['email']).first()

        if not user:
            flash('Email not registered! Please sign up.', 'danger')
            return redirect(url_for('signup.signup'))

        if not check_password_hash(user.password, raw_password):
            flash('Incorrect password! Try again.', 'danger')
            session['login_data'] = form_data
            return redirect(url_for('login.login'))

        login_user(user)
        session.pop('login_data', None)

        if any(role.name == 'admin' for role in user.roles):
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dash.admin_dashboard'))

        flash('Login successful!', 'success')
        return redirect(url_for('user_dash.user_dashboard'))

    form_data = session.pop('login_data', {})
    return render_template('general/login.html', form_data=form_data)
