import os

# Usage:
# import subprocess # just to call an arbitrary command e.g. 'ls'
#
# # enter the directory like this:
# with cd("~/Library"):
#    # we are in ~/Library
#    subprocess.call("ls")
#
# # outside the context manager we are back wherever we started.


class cd:
    """Context manager for changing the current working directory
        http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
    """

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
