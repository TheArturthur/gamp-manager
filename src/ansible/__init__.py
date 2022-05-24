import os

from docker.models.containers import Container

from src import DockerFunctions, run_command_in_container


class Ansible:
    def __init__(self):
        dockerfile_relative_path = 'ansible/docker/'
        dockerfile = ''.join([os.getcwd(), '/', dockerfile_relative_path])
        self.container_ansible_path = '/ansible'
        self.df = DockerFunctions()
        self.df.build_image(path=dockerfile, name='ansible')
        self.ansible_container = self.get_ansible_container()

    def get_ansible_container(self) -> Container:
        return self.df.get_container('ansible')

    def run_ansible_command(self, command: str) -> None:
        run_command_in_container(command, self.ansible_container)

    def run_ansible_playbook(self, playbook: str, inventory: str, hosts: str):
        command = f'ansible-playbook {playbook} {hosts} -i {inventory}'
        run_command_in_container(command, self.ansible_container)
