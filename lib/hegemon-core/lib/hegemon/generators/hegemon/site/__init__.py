import os

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from hegemon.util.file import cd


class SiteBase(object):
    def __init__(self):
        # TODO: Handle the path when base is not in same file!
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.template_path = os.path.join(self.dir, 'templates')
        self.env = Environment(loader=FileSystemLoader(self.template_path))

    def keep_file(self, destination):
        open(destination, 'w').close()

    def empty_directory_with_keep_file(self, destination):
        self.empty_directory(destination)
        self.keep_file(os.path.join(destination, '.keep'))

    def empty_directory(self, destination):
        os.makedirs(destination)

    def path_template(self, path, **kwargs):
        self.template(path, path, **kwargs)

    def template(self, src, dest, **kwargs):
        template = self.env.get_template(src)
        output_from_parsed_template = template.render(kwargs)
        # output_from_parsed_template = template.render(foo='Hello World!')

        # to save the results
        with open(dest, "wb") as fh:
            fh.write(output_from_parsed_template)


class SiteBuilder(SiteBase):
    def __init__(self, args):
        self.args = args
        SiteBase.__init__(self)
        self.generate()

    def generate(self):
        site_name = self.args['<name>']
        self.empty_directory(site_name)
        with cd(site_name):
            for method in "bin config gitignore images lib playbooks roles tmp".split():
                getattr(self, method)()

    def bin(self):
        self.empty_directory('bin')
        self.path_template('bin/hegemon')
        os.chmod('bin/hegemon', 0755)

    def config(self):
        self.empty_directory('config')
        with cd('config'):
            self.empty_directory('environments')
            with cd('environments'):
                self.environment('production')

    def environment(self, name):
        self.empty_directory(name)
        with cd(name):
            self.template('config/environments/{}/hosts'.format(name), 'hosts')
            self.template('config/environments/{}/site.yml'.format(name), 'site.yml')
            self.empty_directory('group_vars')
            with cd('group_vars'):
                self.template('config/environments/{}/group_vars/all.yml'.format(name), 'all.yml')
            self.empty_directory('host_files')
            with cd('host_files'):
                self.empty_directory_with_keep_file('setup_hosts')
            self.empty_directory('host_vars')
            with cd('host_vars'):
                self.template('config/environments/{}/host_vars/setup_hosts.yml'.format(name), 'setup_hosts.yml')

    def gitignore(self):
        self.template('gitignore', '.gitignore')

    def images(self):
        self.empty_directory_with_keep_file('images')

    def lib(self):
        self.empty_directory_with_keep_file('lib')

    def playbooks(self):
        self.empty_directory_with_keep_file('playbooks')

    def roles(self):
        self.empty_directory_with_keep_file('roles')

    def tmp(self):
        self.empty_directory_with_keep_file('tmp')


class SiteGenerator(object):
    #TODO: move this to base class?
    @classmethod
    def start(cls, args):

        #TODO: determine site base path!
        site_base = os.getcwd()
        # site_base = '/tmp'
        with cd(site_base):
            SiteBuilder(args)
