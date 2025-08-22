from flask import render_template, Blueprint
from flask_security import roles_required, current_user
from application.helpers.models import User


admin_view_users_route = Blueprint('admin_view_users', __name__)


@admin_view_users_route.route('/dash/admin/users')
@roles_required('admin')
def users():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('admin/admin_list_users.html', users=users)
