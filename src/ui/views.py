from re import match

from flask import Blueprint, render_template, request, flash, url_for, redirect

from . import db
from .functions import check_form_data_validity, get_exporter_latest_version, create_new_project, template_values
from .models import Projects, Exporters, Targets

views = Blueprint('views', __name__)


@views.route('/', methods=["GET", "POST"])
def start():
    myself = "home.html"
    if request.method == "POST":
        request_form = request.form.to_dict()
        project_name = request_form["project_name"]
        target_name = request_form["target_name"]
        validity_results = check_form_data_validity(request_form)
        print(validity_results)
        print(f'Project: {project_name}, Target: {target_name}')

        if 'project_name' in validity_results[False]:
            flash("The Project name cannot be empty!", category="error")
            return render_template(myself)

        project = Projects.query.filter_by(Name=project_name).first()
        if project is None:
            flash(f"Project \"{project_name}\" was not found in the database! Try adding it.", category="error")
            return render_template(myself, missing=True)

        if 'target_name' in validity_results[False]:
            # all the targets
            project_targets = project.targets
            return render_template(myself, project=project, targets=project_targets)
        elif match(r"(\d+\.){3}\d", target_name):
            # ip
            target = Targets.query.filter_by(project=project_name, IP=target_name).first()
            return render_template(myself, project=project, targets=target, missing=target is None)
        else:
            # hostname
            target = Targets.query.filter_by(project=project_name, Name=target_name).first()
            return render_template(myself, project=project, targets=target, missing=target is None)
    return render_template(myself)


@views.route('/new-project', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        request_form = request.form.to_dict()
        project_name = request_form['project_name']
        project_dc = request_form['project_dc']
        print(f'Name: {project_name}, DC: {project_dc}')
        validity_results = check_form_data_validity(request_form)
        print(validity_results)
        if len(validity_results[False]) == 0:
            create_new_project(project_name, project_dc)
            flash(f"Project {project_name} created in Datacenter {project_dc}", category="success")
            return redirect(url_for("views.start"))
        else:
            for data in validity_results[False]:
                flash(f"{template_values[data]} cannot be empty!", category="error")
    return render_template("new_project.html")


@views.route('/exporters', methods=['GET', 'POST'])
def get_exporters():
    if request.method == 'POST':
        request_form = request.form.to_dict()
        exporter_name = request_form['exporter_name']
        exporter_url = request_form['exporter_url']

        validity_results = check_form_data_validity(request_form)
        if len(validity_results[False]) == 0:
            latest_version = get_exporter_latest_version(exporter_url)
            new_exporter = Exporters(Name=exporter_name, URL=exporter_url, Latest_version=latest_version)
            db.session.add(new_exporter)
            db.session.commit()
            flash(f"Exporter {exporter_name} added to database!", category="success")
            return redirect(url_for("views.start"))
        else:
            for data in validity_results[False]:
                flash(f"{template_values[data]} cannot be empty!", category="error")
    elif request.method == 'GET':
        exporters = Exporters.query.all()

        return render_template("exporters.html", exporters=exporters)
    return render_template("exporters.html")


@views.route('/targets/', methods=['GET', 'POST'])
def targets():
    project_list = Projects.query.all()
    if request.method == 'POST':
        request_form = request.form.to_dict()
        selected_project_name = request_form['list_project_name']
        new_project_name = request_form['project_name']
        new_project_datacenter = request_form['project_dc']

        print(f'Selection: {selected_project_name}, New Name: {new_project_name}, New DC: {new_project_datacenter}')
        validated_results = check_form_data_validity(request_form)
        print(validated_results)

        if selected_project_name == "new_project":
            if len(validated_results[False]) == 0:
                create_new_project(new_project_name, new_project_datacenter)
                flash(f"Project {new_project_name} created in Datacenter {new_project_datacenter}", category="success")
            else:
                for data in validated_results[False]:
                    flash(f"{template_values[data]} cannot be empty!", category="error")
        else:
            new_target_name = request_form['new_target_name']
            new_target_os = request_form['new_target_os']
            new_target_prometheus = request_form['new_target_prometheus']
            new_target_port = request_form['new_target_port']
            new_target_monitoring = request_form['new_target_monitoring']
            new_target_alerting = request_form['new_target_alerting']
            new_target_env = request_form['new_target_env']
            new_target_exporter = request_form['new_target_exporter']

            project = Projects.query.filter_by(Name=selected_project_name).first()
            exporter = Exporters.query.filter_by(Name=new_target_exporter).first()

            new_target = Targets(
                Name=new_target_name,
                OS=new_target_os,
                Prometheus=new_target_prometheus,
                Port=new_target_port,
                Monitoring=new_target_monitoring,
                Alerting=new_target_alerting,
                Environment=new_target_env,
                Project_id=project.idProject,
                Exporter_id=exporter.idExporter
            )

            db.session.add(new_target)
            db.session.commit()
            flash(f"Target {new_target_name} added to project {selected_project_name}", category="success")
    elif request.method == 'GET' and request.form.get('project_name') is not None:
        project = request.args.get('project')
        target_list = Targets.query.filter_by(project=project).all()
        print(target_list)
        return render_template("targets.html", project_list=project_list, target_list=target_list)
    return render_template("targets.html", projects=project_list)
