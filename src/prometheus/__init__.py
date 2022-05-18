import json
import os
import sys
from string import Template

sys.path.append(os.path.abspath("src"))

# targets = ["patatas", "fritas", "con", "huevos", "rotos", "y", "jamon"]
targets = ["a", "las", "patatas", "no", "se", "les", "echa", "ketchup"]

TEST_FILE = 'test.json'
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
          "MONITORING": "$monitoring",
          "PROMETHEUS": "$prometheus",
          "EXPORTER": "$exporter",
          "ALERTING": "$alerting"
        }
      }""")


def create_job():  # target: Targets) -> str:
    """
    Create a job for a target.
    """
    # TODO: Add usage with target from DB.

    new_job = JSON_TEMPLATE.substitute(targets='"{}"'.format('",\n      "'.join(targets)),
                                       jobname="Node Exporter TEST", project="test", environment="TEST",
                                       host="test1", port="9100", monitoring="true", prometheus="nonprod",
                                       exporter="node", alerting="false")

    return new_job


def add_job_to_json():  # target: Targets) -> None:
    """
    Add a job to the json file.
    """
    # TODO: Add usage with target from DB.
    try:
        with open(TEST_FILE, 'r') as file_reader:
            json_file = json.loads(file_reader.read())

        with open(TEST_FILE, 'w') as file_writer:
            new_job = create_job()
            if json_file == []:
                file_writer.write(f"[\n{new_job}\n]")
                return

            new_job_json = json.loads(new_job)
            found_same_job = -1
            for index, job in enumerate(json_file):
                if job['labels'] == new_job_json['labels']:
                    found_same_job = index
                    break
            if found_same_job == -1:
                json_file.append(new_job_json)
            else:  # add targets:
                for target in new_job_json['targets']:
                    if target not in json_file[found_same_job]['targets']:
                        json_file[found_same_job]['targets'].append(target)

            json.dump(json_file, file_writer, indent=2)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(TEST_FILE, 'w') as f:
            f.write('[\n\n]')
        add_job_to_json()


def add_project_rules(project):  # project: Projects) -> None:
    """
    Add rules file for the project from standard.
    """
    # TODO: add rules file for the project from standard.
    with open('standard.yml', 'r') as standard_alerts:
        rules = standard_alerts.read()
    with open(f'{project}_alerts.yml', 'w') as project_alerts:
        rules.replace('PROJECT=""', f'PROJECT="{project}"')
        project_alerts.write(rules)


if __name__ == "__main__":
    add_job_to_json()
    add_project_rules(project="test")
