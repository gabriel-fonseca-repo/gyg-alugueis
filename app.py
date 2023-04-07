from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

dbuser = os.getenv('DB_USER_NAME')
dbpswd = os.getenv('DB_USER_PSWD')

app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI=f'postgresql://{dbuser}:{dbpswd}@localhost/gygalugueis',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='oirodrigues'
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with (app.app_context()):
    db.create_all()
    import routes
