from distutils.core import setup
import glob


setup(
    name='scout',
    version='0.2.7',
    author='various from openSUSE',
    author_email='bernhard+scout-cnf@zq1.de, opensuse-packaging@opensuse.org',
    description=('Indexing openSUSE Linux Packages'),
    long_description="""
      The "command not found" message is not very helpful. If e.g. the
      unzip command is not found but it's available in a package, it
      would be very interesting if the system could tell that the
      command is currently not available, but installing a package
      would provide it.
    """,
    license='MIT',
    url='https://github.com/openSUSE/scout/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='search missing package index',
    packages=['scout'],
    package_dir={'scout': 'scout'},
    package_data={
        'scout': [
            '../data-gen/*', '../doc/*', '../handlers/java/*',
            '../handlers/python/*', '../package/*',
        ]
    },
    data_files=[
        ('etc', ['scout-bash-completion', 'repos.conf',
                 'handlers/bin/command_not_found_bash',
                 'handlers/bin/command_not_found_zsh',
                 'handlers/bin/README']),
        ('i18n/command-not-found', glob.glob('i18n/command-not-found/*.po')),
        ('i18n/scout', glob.glob('i18n/scout/*.po')),
    ],
    scripts=['scout-cmd.py', 'scout-cmd-profile.py',
             'handlers/bin/command-not-found'],
)
