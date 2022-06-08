"""
Base functions to operate with Ansible
"""
import ansible_runner as ar


def run_ansible_playbook(playbook: str, extra_vars: dict, arguments=None):
    """
    Runs playbook in Ansible
    @param playbook route to Ansible playbook
    @param extra_vars Additional variables to pass to playbook
    @param arguments Additional arguments to specify in command
    """
    ar.run(
        private_data_dir="./ansible",
        playbook=playbook,
        extravars=extra_vars,
        cmdline=arguments,
    )
