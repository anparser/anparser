from distutils.core import setup

setup(
    name='anparser',
    version='0.00',
    packages=['anparser', 'anparser.plugins', 'anparser.plugins.xml_plugins', 'anparser.plugins.other_plugins',
              'anparser.plugins.sqlite_plugins', 'anparser.writers'],
    package_data={'anparser': ['tests/test.sqlite', 'tests/test.xml']},
    url='github.com/chapinb/anparser',
    license='GPLv3',
    author='cbryce, pmiller',
    author_email='chapinb@users.noreply.github.com',
    description='Android Artifact Parsing Framework'
)
