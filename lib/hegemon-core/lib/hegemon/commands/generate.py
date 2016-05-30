"""Usage: hegemon [--version] [--no-container] [--help|-h] generate [<args>...]

options:
   -c <name=value>
   -h, --help
   -p, --paginate
The most commonly used git commands are:
   generate        Add file contents to the index
See 'hegemon help <command>' for more information on a specific command.
"""

from docopt import docopt
args = docopt(__doc__, version='0.1.1rc', options_first=True)


print 'HI FROM GENERATE!'