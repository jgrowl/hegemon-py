#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: docker_machine
short_description: Create a local docker host machine using docker-machine
'''

from ansible.module_utils.docker_machine import *


def main():
    module = AnsibleModule(
        argument_spec=docker_machine_argument_spec(
            dict()
        ),
        supports_check_mode=False
    )

    result = DockerMachineModule(module).execute()
    module.exit_json(**result)


from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
