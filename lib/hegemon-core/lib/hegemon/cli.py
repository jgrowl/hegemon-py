import importlib
from hegemon.site_loader import SiteLoader
# from hegemon.commands.command_tasks import CommandTasks

SiteLoader.exec_site()
importlib.import_module('hegemon.commands.site')

# import signal
# import sys
#
# def signal_handler(signal, frame):
#         sys.exit(0)
# signal.signal(signal.SIGINT, signal_handler)

# importlib.import_module('hegemon.commands.site')

# require 'rails/ruby_version_check'
# Signal.trap("INT") { puts; exit(1) }
#
# if ARGV.first == 'plugin'
#   ARGV.shift
#   require 'rails/commands/plugin'
# else
#   require 'rails/commands/application'
# end

