from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

dbuser = os.getenv('DB_USER_NAME')
dbpswd = os.getenv('DB_USER_PSWD')
dbhost = os.getenv('DB_HOST')
dbname = os.getenv('DB_NAME')
dbdriver = os.getenv('DB_DRIVER')
secretkey = os.getenv('SCRKEY')
secpswsalt = os.getenv('SECPSWSALT')

app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI=f'{dbdriver}://{dbuser}:{dbpswd}@{dbhost}/{dbname}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY=secretkey,
    REMEMBER_COOKIE_SAMESITE='strict',
    SESSION_PERMANENT=False,
    SESSION_TYPE="filesystem",
    SESSION_COOKIE_SAMESITE='strict',
)

app.config.update(
    SECURITY_PASSWORD_SALT=secpswsalt,
    SECURITY_LOGIN_URL='/security/login',
    SECURITY_LOGOUT_URL='/security/logout',
    SECURITY_REGISTER_URL='/security/register',
    SECURITY_RESET_URL='/security/reset',
    SECURITY_CHANGE_URL='/security/change',
    SECURITY_CONFIRM_URL='/security/confirm'
)

with (app.app_context()):
    from src.extensions import init_extensions
    init_extensions(app=app)
    import src.orm as orm
    import src.auth as auth
    import src.routes as routes
