from dotenv import dotenv_values
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.backend import check_if_database_exists

db = SQLAlchemy()
USERNAME = "gamp.backend"
PASSWORD = "ContraseñaLarga1234"
SERVER = "192.168.1.148"
PORT = 3306
DB_NAME = "gamp-manager"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/src/backend/gamp-manager.db'
    app.config['SECRET_KEY'] = dotenv_values('secrets/.env')['APP_SECRET_KEY']
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Targets, Projects, Exporters

    if not check_if_database_exists(app):
        db.create_all(app=app)
        print("Database created!")
    else:
        print("Database was not created because it already exists")
    return app
