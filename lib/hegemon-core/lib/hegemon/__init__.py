from __future__ import (absolute_import, division, print_function)

# Based on: https://serversforhackers.com/running-ansible-2-programmatically

import os


def hegemon_lib_home():
    hegemon_lib = os.getenv('HEGEMON_LIB_HOME', None)
    if hegemon_lib is None:
        raise Exception("HEGEMON_LIB_HOME must be defined!")
    return hegemon_lib


def hegemon_home():
    # hegemon_home = os.getenv('HEGEMON_HOME', '/etc/hegemon/sites/default')
    import os
    hegemon_home = os.getenv('HEGEMON_HOME', os.getcwd())
    return hegemon_home

    # hegemon_lib = os.getenv('HEGEMON_LIB_HOME', None)
    # if hegemon_lib is None:
    #     raise Exception("HEGEMON_LIB_HOME must be defined!")
    # return hegemon_lib


class HegemonConfig(object):
    def __init__(self):
        self.hegemon_lib_home = hegemon_lib_home()

        self.hegemon_environment = os.getenv('HEGEMON_ENVIRONMENT', 'production')
        self.hegemon_home = hegemon_home()
        self.hegemon_playbook = os.path.join(self.hegemon_lib_home, 'lib/ansible/playbooks/site.yml')
        self.hegemon_tmp = os.path.join(self.hegemon_home, 'tmp')

        self.config_dir = os.path.join(self.hegemon_home, 'config')
        self.hegemon_configuration = os.path.join(self.config_dir, 'hegemon.yml')
        self.environments_dir = os.path.join(self.config_dir, 'environments')
        self.environment_dir = os.path.join(self.environments_dir, self.hegemon_environment)
        self.site = os.path.join(self.environment_dir, 'site.yml')
        # hosts = os.path.join(environment_dir, 'hosts')
        self.hosts = self.environment_dir

        # os.getenv is equivalent, and can also give a default value instead of `None`
        # private_key_file = os.path.join(environment_dir, 'host_files/setup_hosts/.ssh/id_rsa')
        self.hegemon_run_home = os.path.join(self.environment_dir, 'host_files/setup_hosts')
        self.private_key_file = os.path.join(self.hegemon_run_home, '.ssh/id_rsa')
        self.known_hosts_file = os.path.join(self.hegemon_run_home, '.ssh/known_hosts')

        self.pythonpath = os.getenv('PYTHONPATH', '')

        self.host_files_dir = os.path.join(self.environment_dir, 'host_files')

        self.hegemon_lib_home_bin = os.path.join(self.hegemon_lib_home, 'bin')
        self.path = os.getenv('PATH', '')

        self.hegemon_tmp_path = os.path.join(self.hegemon_home, 'tmp')
        self.hegemon_tmp_env_path = os.path.join(self.hegemon_tmp_path, self.hegemon_environment)

        self.set_environment_variables()

    def set_environment_variables(self):
        # Set Environment Variables
        os.environ["PATH"] = "{}:{}".format(self.path, self.hegemon_lib_home_bin)
        os.environ["PYTHONPATH"] = "{}:{}/lib/python".format(os.getenv('PYTHONPATH', ''), self.hegemon_lib_home)
        os.environ["HOME"] = self.hegemon_run_home

        # Set ANSIBLE_* Environment variables
        os.environ["ANSIBLE_CONFIG"] = os.path.join(self.hegemon_lib_home, 'lib/ansible/ansible.cfg')
        os.environ["ANSIBLE_RETRY_FILES_SAVE_PATH"] = self.hegemon_tmp_env_path
        os.environ["ANSIBLE_LOCAL_TEMP"] = self.hegemon_tmp_env_path
        os.environ["ANSIBLE_SSH_CONTROL_PATH"] = "/tmp/ansible-ssh-%%h-%%p-%%r"
        os.environ["ANSIBLE_ROLES_PATH"] = '/etc/ansible/roles:{}/lib/ansible/roles'.format(self.hegemon_lib_home)


class Hegemon(object):
    def __init__(self, hegemon_config, display):
        self.hegemon_config = hegemon_config
        self.display = display

    def run(self):
        # TODO: make variables called HEGEMON_INTERNAL_* and allow actual variables to be customizable maybe!
        extra_vars = {
            "HEGEMON_HOST_FILES": self.hegemon_config.host_files_dir,
            "HEGEMON_LIB_HOME": self.hegemon_config.hegemon_lib_home,
            "HEGEMON_RUN_HOME": self.hegemon_config.hegemon_run_home,
            "HEGEMON_PYTHONPATH": self.hegemon_config.pythonpath
        }

        ssh_common_args = '-o UserKnownHostsFile=\"{}\"'.format(self.hegemon_config.known_hosts_file)
        ssh_extra_args = ""

        from .runner import Runner
        runner = Runner(
                playbook=self.hegemon_config.hegemon_playbook,
                hosts=self.hegemon_config.hosts,
                display=self.display,
                options={
                    'ssh_common_args': ssh_common_args,
                    'ssh_extra_args': ssh_extra_args,
                    'verbosity': 9,
                    # 'subset': '~^localhost',
                    # 'become': True,
                    # 'become_method': 'sudo',
                    # 'become_user': 'hegemon',
                    # 'private_key_file': private_key_file,
                    # 'tags': 'debug',
                    # 'skip_tags': 'debug',
                    'extra_vars': extra_vars,
                },

                # passwords={
                #     'become_pass': 'sudo_password',
                #     'conn_pass': 'ssh_password',
                # },
                # vault_pass='vault_password',
        )

        stats = runner.run()
        # Maybe do something with stats here? If you want!



