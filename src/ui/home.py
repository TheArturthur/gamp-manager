from re import match

from flask import Blueprint, flash, render_template, request

from .functions import check_form_data_validity
from .models import Projects, Targets

home = Blueprint('home', __name__)


@home.route('/', methods=["GET", "POST"])
def start():
    MYSELF = "home.html"
    if request.method == "POST":
        request_form = request.form.to_dict()
        project_name = request_form["project_name"]
        target_name = request_form["target_name"]
        validity_results = check_form_data_validity(request_form)
        print(validity_results)
        print(f'Project: {project_name}, Target: {target_name}')

        if 'project_name' in validity_results[False]:
            flash("The Project name cannot be empty!", category="error")
            return render_template(MYSELF)

        project = Projects.query.filter_by(Name=project_name).first()
        if project is None:
            flash(f"Project \"{project_name}\" was not found in the database! Try adding it.", category="error")
            return render_template(MYSELF, missing=True)

        if 'target_name' in validity_results[False]:
            # todos los targets
            targets = project.targets
            return render_template(MYSELF, project=project, targets=targets)
        elif match(r"(\d+\.){3}\d", target_name):
            # ip
            target = Targets.query.filter_by(project=project_name, IP=target_name).first()
            return render_template(MYSELF, project=project, targets=target, missing=target is None)
        else:
            # hostname
            target = Targets.query.filter_by(project=project_name, Name=target_name).first()
            return render_template(MYSELF, project=project, targets=target, missing=target is None)
    return render_template(MYSELF)
