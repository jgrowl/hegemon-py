import importlib

from hegemon.command import COMMAND_WHITELIST


class CommandTasks(object):
    @classmethod
    def import_command(cls, command):
        importlib.import_module('hegemon.commands.{}'.format(command))

    def run_command(self, command):
        if command in COMMAND_WHITELIST:
            getattr(self, command)()
        else:
            print 'other task'
            # run_rake_task(command)

    def generate(self):
        print 'generate'

    # def new(self):
    #     #      if %w(-h --help).include?(argv.first)
    #     #   require_command!("application")
    #     # else
    #     #   exit_with_initialization_warning!
    #     # end
    #
    #     self.import_command('site')

    def shell(self):
        self.import_command('shell')

    def run(self):
        self.import_command('run')
