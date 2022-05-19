from re import match
from sys import platform

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
    app.config['SQLALCHEMY_DATABASE_URI'] = generate_database_url()
    app.config['SECRET_KEY'] = 'hvfalkjhvkjfalhgakjfbhvjfalknhvlkjfa'
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


class DatabaseGenerationException(Exception):
    """
    Exception to raise if there's an error while creating the database
    """


def generate_database_url() -> str:
    url = 'sqlite:///{}gamp-manager.db'
    if match(r'linux2?', platform):  # accepts linux and linux2
        return url.format('/home/avidal/git/gamp-manager/src/backend/')
    elif platform == "darwin":
        return url.format('/Users/avidal/git/gamp-manager/src/backend/')
    elif platform == "win32":
        return url.format('C:\\Users\\Arturo Vidal\\Documents\\')
