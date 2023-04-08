from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)

dbuser = os.getenv('DB_USER_NAME')
dbpswd = os.getenv('DB_USER_PSWD')
dbhost = os.getenv('DB_HOST')
dbname = os.getenv('DB_NAME')
dbdriver = os.getenv('DB_DRIVER')

app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI=f'{dbdriver}://{dbuser}:{dbpswd}@{dbhost}/{dbname}',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='oirodrigues',
    SESSION_PERMANENT=False,
    SESSION_TYPE="filesystem"
)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
Session(app)

with (app.app_context()):
    db.create_all()
    import src.routes as routes
