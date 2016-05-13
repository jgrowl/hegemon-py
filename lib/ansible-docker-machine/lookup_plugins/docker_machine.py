from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
import docker_machine


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        client = docker_machine.Client()

        ret = []
        for term in terms:
            if client.machine_name_exists(term):
                machine = client.machine(term)
                default_port = 2376
                value = dict(name=machine.name,
                             docker_url="tcp://{}:{}".format(machine.driver.ip_address, default_port),
                             tls_client_cert=machine.host_options.auth_options.client_cert_path,
                             tls_client_key=machine.host_options.auth_options.client_key_path,
                             tls_ca_cert=machine.host_options.auth_options.ca_cert_path,
                             # use_tls='verify' if machine.host_options.engine_options.tls_verify else 'no'
                             use_tls='encrypt' if machine.host_options.engine_options.tls_verify else 'no',
                             cert_path=machine.host_options.auth_options.store_path,
                             # driver=dict(machine.driver.__dict__),
                             env=machine.env
                             ,private_ip_address=machine.driver.private_ip_address
                             )

                # raise Exception(dict(machine.driver.__dict__)['private_ip_address'])
                ret.append(value)
        return ret
