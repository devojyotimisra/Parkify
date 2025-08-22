from werkzeug.security import generate_password_hash
from application.extensions.db_extn import db
from application.helpers.models import User, Role


def initialize_database(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

        if not Role.query.first():
            admin_role = Role(name='admin')
            user_role = Role(name='user')
            db.session.add_all([admin_role, user_role])
            db.session.commit()

        if not User.query.filter_by(email=app.config["ADMIN_MAIL"]).first():
            admin = User(
                email=app.config["ADMIN_MAIL"],
                password=generate_password_hash(app.config["ADMIN_PASSWORD"]),
                name=app.config["ADMIN_NAME"],
                pincode=app.config["ADMIN_PINCODE"],
                address=app.config["ADMIN_ADDRESS"],
                active=True
            )

            admin_role = Role.query.filter_by(name='admin').first()
            admin.roles.append(admin_role)

            db.session.add(admin)
            db.session.commit()
