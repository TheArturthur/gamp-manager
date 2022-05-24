from urllib import request

from . import db
from .models import Projects


def get_exporter_latest_version(exporter_url) -> str:
    response = request.urlopen(f'{exporter_url}/releases/latest')
    return response.geturl().split('/')[-1]


def check_form_data_validity(form: dict) -> dict:
    result = {True: [], False: []}
    for key, data in form.items():
        result[data is not None and len(data) > 0].append(key)
    return result


def create_new_project(project_name: str, project_dc: str) -> None:
    new_project = Projects(Name=project_name, Datacenter=project_dc)
    db.session.add(new_project)
    db.session.commit()


template_values = {
    'project_name': 'Project Name',
    'project_dc': 'Datacenter',
    'exporter_name': 'Exporter Name',
    'exporter_url': 'Exporter URL',
    'selected_project_name': 'Project Name'
}
