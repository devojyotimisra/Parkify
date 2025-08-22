from flask_security import SQLAlchemyUserDatastore
from application.extensions.security_extn import security
from application.extensions.db_extn import db
from application.helpers.models import User, Role


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def initialize_security(app):
    security.init_app(app, user_datastore)
