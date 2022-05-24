from os import path

from flask import Flask
from sqlalchemy_utils.functions import database_exists


def check_if_database_exists(app: Flask) -> bool:
    database_url: str = app.config['SQLALCHEMY_DATABASE_URI']
    database_path = database_url.split('///')[1]
    return database_exists(database_url) or path.exists(database_path)
