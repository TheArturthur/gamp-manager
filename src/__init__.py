"""
    Base functions and class to submodules operations.
"""
from docker import from_env
from docker.models.containers import Container, ExecResult
from docker.models.images import Image


def run_command_in_container(command: str, container: Container = None) -> ExecResult:
    """
        Allows to run commands in a Docker container
    """
    return container.exec_run(cmd=command)


class DockerFunctions:
    """
        Base Docker functions inside class, allowing base Docker environment definition.
    """

    def __init__(self):
        self.client = from_env()

    def build_image(self, path: str, name: str, tag="latest", remove=True) -> Image:
        """
        Builds docker image based on parameters:
            @param path: Path of Dockerfile from which build image
            @param name: Name of the image to be built.
            @param tag: Tag to apply to the image. Defaults to 'latest'.
            @param remove: Whether to remove previously built image.
            @returns Docker Image built
        """
        image, _ = self.client.images.build(
            path=path, tag="".join([name, ":", tag]), rm=remove
        )
        return image

    def check_if_container_exists(self, name: str) -> bool:
        """
        Returns whether a container exists in Docker
        @param name: Name of container to lookup
        @returns True if container exists; False if not.
        """
        for container in self.client.containers.list(all=True):
            if container.name == name:
                return True
        return False

    def list_containers_from_image(self, image_name: str) -> list:
        """
        Lists containers using specified image
        @param image_name: Name of the image to lookup containers from.
        @returns list of docker containers.
        """
        return self.client.containers.list(all=True, filters={"ancestor": image_name})

    def create_container_from_image(
            self, image: Image, name: str, detach=True, volumes=None
    ) -> Container:
        """
        Creates and run a container with parameters:
        @param image: Docker image to use
        @param name: Name of container
        @param detach: True if container will run detached; False if not.
        @param volumes: Dict of volumes to attach to container
        @returns Docker container created
        """
        return self.client.containers.run(
            image=image,
            detach=detach,
            name=name,
            hostname=name,
            volumes=volumes,
        )

    def get_container(self, name: str) -> Container:
        """
        Returns Docker container by name
        @param name: Name of the container
        @returns Container found by specified name
        """
        return self.client.containers.list(all=True, filters={"name": name})
