from flask import Flask
from flask_cors import CORS

from application.middlewares.init_db import initialize_database
from application.middlewares.init_security import initialize_security
from application.middlewares.init_session import initialize_session
from application.middlewares.init_error import initialize_error_handlers
from application.middlewares.init_cache_control import initialize_cache_control

from application.routes.general.home_route import home_route
from application.routes.general.login_route import login_route
from application.routes.general.logout_route import logout_route
from application.routes.general.signup_route import signup_route

from application.routes.admin.admin_dash_route import admin_dash_route
from application.routes.admin.admin_add_lot_route import admin_add_lot_route
from application.routes.admin.admin_delete_lot_route import admin_delete_lot_route
from application.routes.admin.admin_edit_lot_route import admin_edit_lot_route
from application.routes.admin.admin_history_route import admin_history_route
from application.routes.admin.admin_profile_route import admin_profile_route
from application.routes.admin.admin_profile_edit_route import admin_profile_edit_route
from application.routes.admin.admin_search_route import admin_search_route
from application.routes.admin.admin_view_spot_details_route import admin_view_spot_details_route
from application.routes.admin.admin_view_spots_route import admin_view_spots_route
from application.routes.admin.admin_view_users_route import admin_view_users_route

from application.routes.user.user_book_slot_route import user_book_slot_route
from application.routes.user.user_dash_route import user_dash_route
from application.routes.user.user_history_route import user_history_route
from application.routes.user.user_profile_edit_route import user_profile_edit_route
from application.routes.user.user_profile_route import user_profile_route
from application.routes.user.user_release_slot_route import user_release_slot_route
from application.routes.user.user_search_route import user_search_route
from application.routes.user.user_select_slot_route import user_select_slot_route


app = Flask(__name__)
app.config.from_object("application.helpers.config.Config")
cors = CORS(app)

initialize_database(app)
initialize_security(app)
initialize_session(app)
initialize_error_handlers(app)
initialize_cache_control(app)


app.register_blueprint(home_route)
app.register_blueprint(login_route)
app.register_blueprint(logout_route)
app.register_blueprint(signup_route)

app.register_blueprint(admin_dash_route)
app.register_blueprint(admin_add_lot_route)
app.register_blueprint(admin_delete_lot_route)
app.register_blueprint(admin_edit_lot_route)
app.register_blueprint(admin_history_route)
app.register_blueprint(admin_profile_route)
app.register_blueprint(admin_profile_edit_route)
app.register_blueprint(admin_search_route)
app.register_blueprint(admin_view_spot_details_route)
app.register_blueprint(admin_view_spots_route)
app.register_blueprint(admin_view_users_route)

app.register_blueprint(user_book_slot_route)
app.register_blueprint(user_dash_route)
app.register_blueprint(user_history_route)
app.register_blueprint(user_profile_edit_route)
app.register_blueprint(user_profile_route)
app.register_blueprint(user_release_slot_route)
app.register_blueprint(user_search_route)
app.register_blueprint(user_select_slot_route)


if __name__ == "__main__":
    app.run()
