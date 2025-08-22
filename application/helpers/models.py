from datetime import datetime, timedelta, timezone
from flask_security import UserMixin, RoleMixin
import uuid
from application.extensions.db_extn import db


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)


user_roles = db.Table('user_roles',db.Column('user_id', db.Integer(), db.ForeignKey('users.id')), db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    pincode = db.Column(db.String(7), nullable=False)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, default=lambda: str(uuid.uuid4()))
    vehicle_number = db.Column(db.String(20), unique=True)

    roles = db.relationship('Role', secondary=user_roles, backref='users')
    reservations = db.relationship('ReserveParkingSpot', backref='user',lazy=True, order_by='ReserveParkingSpot.parking_timestamp.desc()')

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)


class ParkingLot(db.Model):
    __tablename__ = "parking_lots"
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prime_location_name = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(256), nullable=False)
    pin_code = db.Column(db.String(7), nullable=False)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone(timedelta(hours=5, minutes=30))))

    parking_spots = db.relationship('ParkingSpot', backref='lot', lazy=True, cascade="all, delete-orphan")

    @property
    def available_spots_count(self):
        return ParkingSpot.query.filter_by(lot_id=self.id, status='A').count()

    @property
    def occupied_spots_count(self):
        return ParkingSpot.query.filter_by(lot_id=self.id, status='O').count()


class ParkingSpot(db.Model):
    __tablename__ = "parking_spots"
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')

    reservations = db.relationship('ReserveParkingSpot', backref='spot', lazy=True)


class ReserveParkingSpot(db.Model):
    __tablename__ = "reserved_parking_spots"
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id = db.Column(db.Integer)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime)
    parking_cost_per_unit_time = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float)
    duration_hours = db.Column(db.Float)
