# -*- coding: utf-8 -*-

import os
import re
import setuptools

dirname = os.path.dirname(__file__)

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Determine version number automatically
version = ''
with open(os.path.join(dirname, 'rest_roles', '__init__.py')) as module_file:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        module_file.read(),
        re.MULTILINE
    ).group(1)

# Read in description info from files
with open(os.path.join(dirname, 'README.md')) as readme_file:
    readme = readme_file.read()
with open(os.path.join(dirname, 'HISTORY.md')) as history_file:
    history = history_file.read()

# Organize requirements
install_requires = [
    'djangorestframework>=3.0',
    'six',
]
tests_requires = [
    'pytest',
    'mock',
    'virtualenv',
]

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
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
