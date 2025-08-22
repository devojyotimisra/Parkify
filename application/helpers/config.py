from os import getenv
from datetime import timedelta
from dotenv import load_dotenv


load_dotenv()


class Config:
    FLASK_DEBUG = getenv("FLASK_DEBUG") == "True"
    FLASK_RUN_HOST = getenv("FLASK_RUN_HOST")
    FLASK_RUN_PORT = getenv("FLASK_RUN_PORT")

    SECRET_KEY = getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv("SQLALCHEMY_TRACK_MODIFICATIONS") == "True"

    PERMANENT_SESSION_LIFETIME = timedelta(seconds=int(getenv('SECONDS')))

    ADMIN_MAIL = getenv("ADMIN_MAIL")
    ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")
    ADMIN_NAME = getenv("ADMIN_NAME")
    ADMIN_PINCODE = int(getenv("ADMIN_PINCODE"))
    ADMIN_ADDRESS = getenv("ADMIN_ADDRESS")

    SESSION_REFRESH_EACH_REQUEST = getenv("SESSION_REFRESH_EACH_REQUEST") == "True"
    SESSION_PERMANENT = getenv("SESSION_PERMANENT") == "True"

    SECURITY_LOGIN_URL = getenv("SECURITY_LOGIN_URL")
    SECURITY_LOGOUT_URL = getenv("SECURITY_LOGOUT_URL")
    SECURITY_REGISTERABLE = getenv("SECURITY_REGISTERABLE") == "True"
    SECURITY_SEND_REGISTER_EMAIL = getenv("SECURITY_SEND_REGISTER_EMAIL") == "True"
    SECURITY_USERNAME_ENABLE = getenv("SECURITY_USERNAME_ENABLE") == "True"
