"""Usage: hegemon [--version] [--skip-container] [--help|-h] <command> [<args>...]

options:
   -h, --help
   -v
The most commonly used git commands are:
   new             Generate a new project
   generate        Generate basic configuration or other files
   shell
   console
   server
See 'hegemon help <command>' for more information on a specific command.
"""

from docopt import docopt


COMMAND_WHITELIST = 'generate new shell run'.split()

args = docopt(__doc__, version='0.1.1rc', options_first=True)
if args['--skip-container']:
    command = args['<command>']
    if command in COMMAND_WHITELIST:
        from hegemon.commands.command_tasks import CommandTasks
        CommandTasks().run_command(command)
    elif command in ['help', None]:
        print 'TODO: Show help'
    else:
        exit("%r is not a hegemon command. See 'hegemon help'." % args['<command>'])
else:
    import sys
    import os
    from docker import Client
    import dockerpty
    import getpass
    from pwd import getpwnam
    from docker.utils import create_host_config
    from hegemon import hegemon_lib_home, hegemon_home

    cwd = os.getcwd()

    hegemon_lib_home = hegemon_lib_home()
    sys.path.append('{}/lib/python'.format(hegemon_lib_home))

    hegemon_home = hegemon_home()

    # src = '/usr/bin/python'
    # dst = '/tmp/python'
    #
    # # This creates a symbolic link on python in tmp directory
    # os.symlink(src, dst)
    # directory = ''
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    username = getpass.getuser()
    uid = getpwnam(username)[2]
    guid = getpwnam(username).pw_uid
    display = None

    # base_url = 'tcp://127.0.0.1:2375'
    base_url = 'unix://var/run/docker.sock'
    image = 'jgrowl/hegemon'
    cli = Client(base_url=base_url)

    hegemon_args = sys.argv[1:] if len(sys.argv) > 1 else []
    hegemon_args.insert(0, '--skip-container')

    site_name = ''
    if args['<command>'] == 'new':
        site_name = 'hegemon_new_{}'.format(args['<args>'][0])
    else:
        site_name = 'hegemon_{}'.format(os.path.basename(os.path.normpath(cwd)))

    volumes = [
        cwd,
        '/var/run/docker.sock',
        '/var/lib/docker'
    ]

    environment = {
        'HEGEMON_UID': uid,
        'HEGEMON_GUID': guid
    }

    host_config = create_host_config(binds=[
        '{}:{}'.format(cwd, cwd),
        '/var/run/docker.sock:/var/run/docker.sock',
        '/var/lib/docker:/var/lib/docker'
    ])

    container = cli.create_container(
            image=image,
            stdin_open=True,
            tty=True, command=" ".join(hegemon_args),
            volumes=volumes,
            environment=environment,
            name=site_name,
            host_config=host_config,
            working_dir=cwd
    )

    dockerpty.start(cli, container)
    cli.remove_container(container)

    # print arguments



