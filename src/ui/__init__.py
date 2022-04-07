from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists
from os import path

db = SQLAlchemy()
USERNAME="gamp.backend"
PASSWORD="ContraseñaLarga1234"
SERVER="192.168.1.148"
PORT=3306
DB_NAME="gamp-manager"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'njfasñbvfjnkabv fasvfagñvfa'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{USERNAME}:{PASSWORD}@{SERVER}:{PORT}/{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Targets, Projects, Exporters

    create_database(app)

    return app

def create_database(app):
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all(app=app)
        print("Database created")