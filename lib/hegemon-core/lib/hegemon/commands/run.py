"""Usage: hegemon [--version] [--skip-container] [--help|-h] run

options:
   -h, --help
   -p, --paginate
The most commonly used git commands are:
   new        Add file contents to the index
See 'hegemon help <command>' for more information on a specific command.
"""

import os

from docopt import docopt
args = docopt(__doc__, version='0.1.1rc', options_first=True)

from hegemon import Hegemon
from hegemon import HegemonConfig

hegemon_config = HegemonConfig()

# It's important that all ANSIBLE_* configuration environment variables come before a Display is created
from ansible.utils.display import Display
display = Display()

hegemon = Hegemon(hegemon_config, display)
hegemon.run()
