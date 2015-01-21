# -*- coding: utf-8 -*-

from distutils.core import setup
from pip.req import parse_requirements

# Parses the requirements.txt
install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='anparser',
    version='0.00',
    packages=['anparser', 'anparser.plugins', 'anparser.plugins.xml_plugins', 'anparser.plugins.other_plugins',
              'anparser.plugins.sqlite_plugins', 'anparser.writers'],
    package_data={'anparser': ['tests/test.sqlite', 'tests/test.xml']},
    url='github.com/chapinb/anparser',
    license='GPLv3',
    install_reqs=reqs,
    author='cbryce, pmiller',
    author_email='chapinb@users.noreply.github.com',
    description='Android Artifact Parsing Framework'
)