"""
Base functions to operate with database.
"""
from src.ui import db
from src.ui.models import Exporters


def add_exporter(exporter_name, exporter_url, exporter_version):
    """
    Adds new exporter to database
    @param exporter_name Name of exporter
    @param exporter_url URL to obtain exporter bin and version
    @param exporter_version The latest exporter version available
    """
    exporter = Exporters(
        Name=exporter_name, URL=exporter_url, Latest_version=exporter_version
    )
    db.session.add(exporter)
    db.session.commit()


def get_all_exporters():
    """
    Returns all exporters in the database
    """
    return Exporters.query.all()
