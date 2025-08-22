from flask import render_template, redirect, url_for, Blueprint
from flask_security import current_user


home_route = Blueprint('home', __name__)


@home_route.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('general/index.html')

    if current_user.has_role('admin'):
        return redirect(url_for('admin_dash.admin_dashboard'))
    return redirect(url_for('user_dash.user_dashboard'))
