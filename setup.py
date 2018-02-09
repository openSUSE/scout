#!/usr/bin/python
import os
from setuptools import setup

setup(
    name = 'scout',
    version = '0.1.2.dev1',
    author = 'various from openSUSE',
    author_email = 'bernhard+scout-cnf zq1 dot de ; opensuse-packaging at opensuse.org',
    description = ('Indexing openSUSE Linux Packages'),
    long_description = """
      The "command not found" message is not very helpful. If e.g. the unzip
      command is not found but it's available in a package, it would be very
      interesting if the system could tell that the command is currently not
      available, but installing a package would provide it.
    """,
    license = 'MIT',
    url = 'https://github.com/openSUSE/scout/',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords = "search missing package index",
    packages = ['scout'],
    package_data = {
        'scout': [
            '../data-gen/*', '../doc/*', '../handlers/*', '../i18n/*',
            '../package/*', '../repos.conf',
        ]
    },
    data_files = [
        ('etc', ['scout-bash-completion']),
        ('config', ['repos.conf']),
    ],
    scripts = ['scout-cmd.py', 'scout-cmd-profile.py'],
)
