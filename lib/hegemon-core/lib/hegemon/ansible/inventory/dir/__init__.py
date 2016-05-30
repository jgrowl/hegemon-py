# (c) 2013, Daniel Hokka Zakrisson <daniel@hozac.com>
# (c) 2014, Serge van Ginderachter <serge@vanginderachter.be>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

#############################################
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.utils.vars import combine_vars

#FIXME: make into plugins
from ansible.inventory.ini import InventoryParser as InventoryINIParser
from ansible.inventory.yaml import InventoryParser as InventoryYAMLParser
from ansible.inventory.script import InventoryScript
from ansible.inventory.dir import get_file_parser, InventoryDirectory


class HegemonInventoryDirectory(InventoryDirectory):
    ''' Host inventory parser for ansible using a directory of inventories. '''

    def __init__(self, loader, groups=None, filename=C.DEFAULT_HOST_LIST):
        if groups is None:
            groups = dict()

        self.names = os.listdir(filename)
        self.names.sort()
        self.directory = filename
        self.parsers = []
        self.hosts = {}
        self.groups = groups

        self._loader = loader

        for i in self.names:

            # Skip files that end with certain extensions or characters
            if any(i.endswith(ext) for ext in C.DEFAULT_INVENTORY_IGNORE):
                continue
            # Skip hidden files
            if i.startswith('.') and not i.startswith('./'):
                continue
            # These are things inside of an inventory basedir
            if i in ("host_vars", "group_vars", "vars_plugins"):
                continue
            fullpath = os.path.join(self.directory, i)
            if os.path.isdir(fullpath):
                parser = InventoryDirectory(loader=loader, groups=groups, filename=fullpath)
            else:
                parser = get_file_parser(fullpath, self.groups, loader)
                if parser is None:
                    #FIXME: needs to use display
                    import warnings
                    warnings.warning("Could not find parser for %s, skipping" % fullpath)
                    continue

            self.add_parser(parser)

        # Hegemon specific host files
        # TODO: put in config file to choose what you want
        for i in ['machine_hosts.py']:
            folder = os.path.dirname(os.path.realpath(__file__))
            hostfile = os.path.join(folder, i)
            parser = get_file_parser(hostfile, self.groups, loader)
            self.add_parser(parser)
            pass

        # extra checks on special groups all and ungrouped
        # remove hosts from 'ungrouped' if they became member of other groups
        if 'ungrouped' in self.groups:
            ungrouped = self.groups['ungrouped']
            # loop on a copy of ungrouped hosts, as we want to change that list
            for host in frozenset(ungrouped.hosts):
                if len(host.groups) > 1:
                    host.groups.remove(ungrouped)
                    ungrouped.hosts.remove(host)

        # remove hosts from 'all' if they became member of other groups
        # all should only contain direct children, not grandchildren
        # direct children should have dept == 1
        if 'all' in self.groups:
            allgroup = self.groups['all' ]
            # loop on a copy of all's  child groups, as we want to change that list
            for group in allgroup.child_groups[:]:
                # groups might once have beeen added to all, and later be added
                # to another group: we need to remove the link wit all then
                if len(group.parent_groups) > 1 and allgroup in group.parent_groups:
                    # real children of all have just 1 parent, all
                    # this one has more, so not a direct child of all anymore
                    group.parent_groups.remove(allgroup)
                    allgroup.child_groups.remove(group)
                elif allgroup not in group.parent_groups:
                    # this group was once added to all, but doesn't list it as
                    # a parent any more; the info in the group is the correct
                    # info
                    allgroup.child_groups.remove(group)

    def add_parser(self, parser):
        self.parsers.append(parser)

        # retrieve all groups and hosts form the parser and add them to
        # self, don't look at group lists yet, to avoid
        # recursion trouble, but just make sure all objects exist in self
        newgroups = parser.groups.values()
        for group in newgroups:
            for host in group.hosts:
                self._add_host(host)
        for group in newgroups:
            self._add_group(group)

        # now check the objects lists so they contain only objects from
        # self; membership data in groups is already fine (except all &
        # ungrouped, see later), but might still reference objects not in self
        for group in self.groups.values():
            # iterate on a copy of the lists, as those lists get changed in
            # the loop
            # list with group's child group objects:
            for child in group.child_groups[:]:
                if child != self.groups[child.name]:
                    group.child_groups.remove(child)
                    group.child_groups.append(self.groups[child.name])
            # list with group's parent group objects:
            for parent in group.parent_groups[:]:
                if parent != self.groups[parent.name]:
                    group.parent_groups.remove(parent)
                    group.parent_groups.append(self.groups[parent.name])
            # list with group's host objects:
            for host in group.hosts[:]:
                if host != self.hosts[host.name]:
                    group.hosts.remove(host)
                    group.hosts.append(self.hosts[host.name])
                # also check here that the group that contains host, is
                # also contained in the host's group list
                if group not in self.hosts[host.name].groups:
                    self.hosts[host.name].groups.append(group)
