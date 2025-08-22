from flask import render_template, Blueprint
from flask_security import roles_required


user_profile_route = Blueprint('user_profile', __name__)


@user_profile_route.route('/dash/user/profile')
@roles_required('user')
def profile():
    return render_template('user/user_profile.html')
