import os
import os.path
import sys
import subprocess


class SiteLoader(object):

    # EXECUTABLES = ['bin/hegemon']
    EXECUTABLE = 'bin/hegemon'

    @classmethod
    def exec_site(cls):
        original_cwd = os.getcwd()

        while True:
            if os.path.isfile(cls.EXECUTABLE):
                # Maybe use exec here?
                subprocess.call([cls.EXECUTABLE] + sys.argv[1:])
                quit()

                # contents = True
                # contents = File.read(exe)
                # if contents =~ /(APP|ENGINE)_PATH/
                #   exec RUBY, exe, *ARGV
                #   break # non reachable, hack to be able to stub exec in the test suite
                # elsif exe.end_with?('bin/rails') && contents.include?('This file was generated by Bundler')
                #   $stderr.puts(BUNDLER_WARNING)
                #   Object.const_set(:APP_PATH, File.expand_path('config/application', Dir.pwd))
                #   require File.expand_path('../boot', APP_PATH)
                #   require 'rails/commands'
                #   break
                # end

            # If we exhaust the search there is no executable, this could be a
            # call to generate a new application, so restore the original cwd.
            # http://stackoverflow.com/questions/9823143/check-if-a-directory-is-a-file-system-root
            cwd = os.getcwd()
            is_root = os.path.dirname(cwd) == cwd
            if is_root:
                os.chdir(original_cwd)
                return False

            # Otherwise keep moving upwards in search of an executable.
            os.chdir('..')
