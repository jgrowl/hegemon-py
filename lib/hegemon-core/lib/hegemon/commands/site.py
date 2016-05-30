"""Usage: hegemon [--version] [--skip-container] [--help|-h] new <name>

options:
   -h, --help
   -p, --paginate
The most commonly used git commands are:
   new        Add file contents to the index
See 'hegemon help <command>' for more information on a specific command.
"""

from docopt import docopt

from hegemon.generators.hegemon.site import SiteGenerator
args = docopt(__doc__, version='0.1.1rc', options_first=True)
SiteGenerator.start(args)
