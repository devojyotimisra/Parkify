from flask import render_template, Blueprint
from flask_security import roles_required


admin_profile_route = Blueprint('admin_profile', __name__)


@admin_profile_route.route('/dash/admin/profile')
@roles_required('admin')
def profile():
    return render_template('admin/admin_profile.html')
