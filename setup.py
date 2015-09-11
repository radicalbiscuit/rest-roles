# -*- coding: utf-8 -*-

import os
import re
import setuptools
import sys
from setuptools.command.test import test

# Hard links don't work inside VirtualBox shared folders. In order to allow
# setup.py sdist to work in such an environment, this quick and dirty hack is
# used. See http://stackoverflow.com/a/22147112.
if os.path.abspath(__file__).split(os.path.sep)[1] == 'vagrant':
    del os.link

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Determine version number automatically
dirname = os.path.dirname(__file__)
version = ''
with open(os.path.join(dirname, 'rest_roles', '__init__.py')) as module_file:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        module_file.read(),
        re.MULTILINE
    ).group(1)

# Read in description info from files
with open(os.path.join(dirname, 'README.rst')) as readme_file:
    readme = readme_file.read()
with open(os.path.join(dirname, 'HISTORY.rst')) as history_file:
    history = history_file.read()

# Organize requirements
install_requires = [
    'djangorestframework>=3.0',
]
tests_requires = [
    'tox',
]


class Tox(test):
    """Use tox when running setup.py test."""

    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        test.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


# Main setup command
setuptools.setup(
    name='restroles',
    version=version,
    description=(
        'Role-based authentication and permissions for Django REST Framework'),
    long_description=readme + '\n\n' + history,
    author='Jeff Schenck',
    author_email='jmschenck@gmail.com',
    url='https://github.com/jeffschenck/rest-roles',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_requires,
    cmdclass={'test': Tox},
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
