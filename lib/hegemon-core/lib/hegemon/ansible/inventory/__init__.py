from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.inventory import Inventory
from ansible import constants as C


import fnmatch
import os
import sys
import re
import itertools

from ansible.compat.six import string_types

from ansible import constants as C
from ansible.errors import AnsibleError

from hegemon.ansible.inventory.dir import HegemonInventoryDirectory
from ansible.inventory.dir import InventoryDirectory, get_file_parser
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.plugins import vars_loader
from ansible.utils.unicode import to_unicode, to_bytes
from ansible.utils.vars import combine_vars
from ansible.parsing.utils.addresses import parse_address


class HegemonInventory(Inventory):

    def __init__(self, loader, variable_manager, host_list=C.DEFAULT_HOST_LIST):
        # super(Inventory, self).__init__(loader, variable_manager, host_list)
        Inventory.__init__(self, loader, variable_manager, host_list)


    def parse_inventory(self, host_list):
        if isinstance(host_list, string_types):
            if "," in host_list:
                host_list = host_list.split(",")
                host_list = [ h for h in host_list if h and h.strip() ]

        self.parser = None

        # Always create the 'all' and 'ungrouped' groups, even if host_list is
        # empty: in this case we will subsequently an the implicit 'localhost' to it.

        ungrouped = Group('ungrouped')
        all = Group('all')
        all.add_child_group(ungrouped)

        self.groups = dict(all=all, ungrouped=ungrouped)

        if host_list is None:
            pass
        elif isinstance(host_list, list):
            for h in host_list:
                try:
                    (host, port) = parse_address(h, allow_ranges=False)
                except AnsibleError as e:
                    display.vvv("Unable to parse address from hostname, leaving unchanged: %s" % to_unicode(e))
                    host = h
                    port = None
                all.add_host(Host(host, port))
        elif self._loader.path_exists(host_list):
            #TODO: switch this to a plugin loader and a 'condition' per plugin on which it should be tried, restoring 'inventory pllugins'
            if self.is_directory(host_list):
                # Ensure basedir is inside the directory
                host_list = os.path.join(self.host_list, "")
                # self.parser = InventoryDirectory(loader=self._loader, groups=self.groups, filename=host_list)
                self.parser = HegemonInventoryDirectory(loader=self._loader, groups=self.groups, filename=host_list)
            else:
                self.parser = get_file_parser(host_list, self.groups, self._loader)
                vars_loader.add_directory(self.basedir(), with_subdir=True)

            if not self.parser:
                # should never happen, but JIC
                raise AnsibleError("Unable to parse %s as an inventory source" % host_list)
        else:
            display.warning("Host file not found: %s" % to_unicode(host_list))

        self._vars_plugins = [ x for x in vars_loader.all(self) ]

        # set group vars from group_vars/ files and vars plugins
        for g in self.groups:
            group = self.groups[g]
            group.vars = combine_vars(group.vars, self.get_group_variables(group.name))

        # set host vars from host_vars/ files and vars plugins
        for host in self.get_hosts():
            host.vars = combine_vars(host.vars, self.get_host_variables(host.name))


