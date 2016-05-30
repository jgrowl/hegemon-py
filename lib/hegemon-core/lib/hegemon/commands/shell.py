"""Usage: hegemon [--version] [--skip-container] [--help|-h] shell

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

# If you need to jump into a shell for debugging purposes!
os.system("(cd ~; /bin/sh)")
