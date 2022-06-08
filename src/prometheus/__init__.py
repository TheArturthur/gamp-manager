import json
import os
import sys
from string import Template

from src.ansible import run_ansible_playbook
from src.ui.models import Targets

sys.path.append(os.path.abspath("src"))

TARGETS_PATH = os.path.abspath(
    os.getcwd() + "/src/prometheus/prometheus-server/targets/"
)
RULES_PATH = os.path.abspath(os.getcwd() + "/src/prometheus/prometheus-server/rules/")
STANDARD_RULES_PATH = os.path.abspath(
    os.getcwd() + "/src/prometheus/prometheus-server/rules/standard.yml"
)

JSON_TEMPLATE = Template(
    """  {
        "targets": [
          $targets
        ],
        "labels": {
          "jobname": "$jobname",
          "PROJECT": "$project",
          "ENVIRONMENT": "$environment",
          "HOST": "$host",
          "PORT": "$port",
          "OS": "$os",
          "MONITORING": "$monitoring",
          "PROMETHEUS": "$prometheus",
          "EXPORTER": "$exporter",
          "ALERTING": "$alerting"
        }
      }"""
)


def ansible_add_host_to_inventory(target: Targets):
    playbook_arguments = '--tags "inventory"'
    extra_vars = {"target_name": target.Name}
    run_ansible_playbook(
        playbook="prometheus.yml", extra_vars=extra_vars, arguments=playbook_arguments
    )


def ansible_install_exporter(target: Targets, exporter_version: str) -> None:
    arguments = f"--limit {target.Name}"
    extra_vars = {"exporter_version": exporter_version}
    run_ansible_playbook(
        playbook="node_exporter.yml", extra_vars=extra_vars, arguments=arguments
    )


def add_new_project_to_prometheus(
        target: Targets, exporter_name: str, project_name: str
) -> None:
    new_job = __create_job__(
        target=target, exporter_name=exporter_name, project_name=project_name
    )
    __add_job_to_json__(
        new_job=new_job, exporter_name=exporter_name, project_name=project_name
    )
    # __add_project_rules__(project_name=project_name)


def __create_job__(target: Targets, exporter_name: str, project_name: str) -> str:
    """
    Create a job for a target.
    """
    json_targets = ":".join([target.Name, str(target.Port)])

    new_job = JSON_TEMPLATE.substitute(
        targets='"{}"'.format('",\n      "'.join([json_targets])),
        jobname=" ".join([exporter_name, target.Environment]),
        project=project_name,
        environment=target.Environment,
        host=target.Name,
        port=target.Port,
        os=target.OS,
        monitoring=target.Monitoring,
        prometheus=target.Prometheus,
        exporter=exporter_name,
        alerting=target.Alerting,
    )
    return new_job


def __add_job_to_json__(new_job: str, exporter_name: str, project_name: str) -> None:
    """
    Add a job to the json file.
    """
    json_file_path = TARGETS_PATH + f"/{project_name}.json"
    try:
        with open(json_file_path, "r") as file_reader:
            json_file = json.loads(file_reader.read())

        with open(json_file_path, "w") as file_writer:
            if not json_file:
                file_writer.write(f"[\n{new_job}\n]")
                return

            new_job_json = json.loads(new_job)
            found_same_job = -1
            for index, job in enumerate(json_file):
                if job["labels"] == new_job_json["labels"]:
                    found_same_job = index
                    break
            if found_same_job == -1:
                json_file.append(new_job_json)
            else:  # add targets:
                for target in new_job_json["targets"]:
                    if target not in json_file[found_same_job]["targets"]:
                        json_file[found_same_job]["targets"].append(target)

            json.dump(json_file, file_writer, indent=2)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(json_file_path, "w") as f:
            f.write("[\n\n]")
        __add_job_to_json__(
            new_job=new_job, exporter_name=exporter_name, project_name=project_name
        )


def __add_project_rules__(project_name: str) -> None:
    """
    Add rules file for the project from standard.
    """
    rules_file_path = RULES_PATH + f"{project_name}_alerts.yml"
    with open(STANDARD_RULES_PATH, "r") as standard_alerts:
        rules = standard_alerts.read()
    with open(rules_file_path, "w") as project_alerts:
        rules.replace('PROJECT=""', f'PROJECT="{project_name}"')
        project_alerts.write(rules)
