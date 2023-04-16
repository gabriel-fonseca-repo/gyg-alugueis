from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.models import fsqla_v3 as fsqla

db = SQLAlchemy()
login_manager = LoginManager()
session = Session()
migrate = Migrate()
security = Security()

def init_extensions(app):
    db.init_app(app=app)
    fsqla.FsModels.set_db_info(appdb=db)
    app.security = security

    from src.orm import User, Role
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security.init_app(app, datastore)

    migrate.init_app(app, db)
    session.init_app(app=app)
    login_manager.init_app(app=app)

