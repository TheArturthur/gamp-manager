import ansible_runner as ar
import pathlib
from os import getcwd

ar.get_inventory("graph", [pathlib.Path(getcwd()).parent.parent.joinpath('ansible\\inventory\\inventory.yml')])


