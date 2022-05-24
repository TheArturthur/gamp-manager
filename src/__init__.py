from docker import from_env
from docker.models.containers import Container
from docker.models.images import Image


def run_command_in_container(command: str, container: Container = None) -> None:
    container.exec_run(cmd=command)


class DockerFunctions:
    def __init__(self):
        self.client = from_env()

    def build_image(self, path: str, name: str, tag='latest', rm=True) -> Image:
        image, log = self.client.images.build(path=path, tag=''.join([name, ':', tag]), rm=rm)
        return image

    def check_if_container_exists(self, name: str) -> bool:
        for container in self.client.containers.list(all=True):
            if container.name == name:
                return True
        return False

    def list_containers_from_image(self, image_name: str) -> list:
        return self.client.containers.list(all=True, filters={"ancestor": image_name})

    def create_container_from_image(self, image: Image, name: str, hostname='', detach=True, volumes=None) -> Container:
        return self.client.containers.run(image=image, detach=detach, name=name,
                                          hostname=hostname if hostname != '' else name, volumes=volumes)

    def get_container(self, name: str) -> Container:
        return self.client.containers.list(all=True, filters={"name": name})
