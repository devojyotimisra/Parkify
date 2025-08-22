from flask import redirect, url_for, Blueprint, flash
from flask_security import logout_user


logout_route = Blueprint('logout', __name__)


@logout_route.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home.index'))
