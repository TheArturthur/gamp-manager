"""
Base database functions to operate with SQLAlchemy
"""
from os import path

from flask import Flask
from sqlalchemy_utils.functions import database_exists


def check_if_database_exists(app: Flask) -> bool:
    """
        Checks if database exists in app
        @param app: Flask app to check the database
        @returns True if it exists; False if not.
        """
    database_url: str = app.config["SQLALCHEMY_DATABASE_URI"]
    database_path = database_url.split("///")[1]
    return database_exists(database_url) or path.exists(database_path)
