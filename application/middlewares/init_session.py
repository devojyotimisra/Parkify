from application.extensions.session_extn import configure_session_management


def initialize_session(app):
    configure_session_management(app)
