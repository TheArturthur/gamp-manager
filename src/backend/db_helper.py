from src.ui import db
from src.ui.models import Exporters


def add_exporter(exporter_name, exporter_url, exporter_version):
    exporter = Exporters(Name=exporter_name, URL=exporter_url, Latest_version=exporter_version)
    db.session.add(exporter)
    db.session.commit()


def get_all_exporters():
    return Exporters.query.all()
