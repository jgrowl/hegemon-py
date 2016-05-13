from __future__ import absolute_import

import docker_machine

from docker_machine.cli.driver_config import (
    create_config_from_dict,
    list_supported_drivers
)


from docker_machine.errors import (
    MissingRequiredArgument,
    UnknownDriverException,
    DockerMachineException
)

class DockerMachineModule(object):
    def __init__(self, module, driver):
        self.module = module
        self.driver = driver

        args = module.params
        self.state = args['state']
        self.name = args['name']
        self.status = None
        self.client = None
        self.driver_config = args.copy()
        for k in ['state', 'name']:
            self.driver_config.pop(k)

    def execute(self):
        try:
            self.client = docker_machine.Client()
            self.driver_config = create_config_from_dict(self.driver, self.driver_config)

            if self.client.machine_name_exists(self.name):
                self.status = self.client.machine_status(self.name)

            if self.state == 'running' and self.status is None:
                self.client.create_machine(self.name, self.driver_config)
                return dict(changed=True)
            elif self.state == 'absent' and self.status is not None:
                self.client.remove_machine(self.name, force=True)
                return dict(changed=True)
            return dict(changed=False)
        except MissingRequiredArgument as e:
            return dict(changed=False, failed=True, msg="missing required arguments: {}".format(e.arg_name))
        except UnknownDriverException:
            return dict(changed=False, failed=True, msg="value of driver must be one of: {} got: {}".format(', '.join(list_supported_drivers()), self.driver))
        except DockerMachineException as e:
            return dict(changed=False, failed=True, msg=e.message)


def docker_machine_argument_spec(driver_arg_specs=None):
    required_arg_specs = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', choices=['running', 'absent'])
    )

    if driver_arg_specs is not None:
        required_arg_specs.update(driver_arg_specs)

    return required_arg_specs
