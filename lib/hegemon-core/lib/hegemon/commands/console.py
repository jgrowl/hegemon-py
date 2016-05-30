"""Usage: hegemon [--version] [--no-container] [--help|-h] console

options:
   -h, --help
   -p, --paginate
The most commonly used git commands are:
   new        Add file contents to the index
See 'hegemon help <command>' for more information on a specific command.
"""

from docopt import docopt
args = docopt(__doc__, version='0.1.1rc', options_first=True)

print 'TODO: implement hegemon console'

