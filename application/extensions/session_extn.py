from flask import session
from flask_security import current_user


def configure_session_management(app):
    @app.before_request
    def auto_permanent_session():
        if current_user.is_authenticated:
            session.permanent = True
