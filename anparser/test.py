__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '20150113'
__version__ = '0.00'

"""
anparser - an Open Source Android Artifact Parser
Copyright (C) 2015  Chapin Bryce

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest

from plugins import xml_plugins
from plugins import sqlite_plugins
from plugins import other_plugins
from writers import csv_writer


class TestAnParser(unittest.TestCase):

    def setUp(self):
        pass

    def test_xmlFiles(self):
        self.xml_return = xml_plugins.parse_xml_file_notree('tests/test.xml')

        self.expected_data = [{'name': 'ds__downloads_json__',
                          'text_entry': '[{"minVersion":0,"filename":"libAppDataSearchExt_armeabi_v7a.so",'
                                        '"sizeBytes":3810616}]'},
                         {'name': 'libAppDataSearchExt_armeabi_v7a.so__dest__', 'text_entry': 'None'},
                         {'name': 'ds__next_alarm__', 'value': '178309873', 'text_entry': 'None'}]

        self.assertEqual(self.xml_return, self.expected_data)

    def test_sqliteGetTableNames(self):
        self.sqlite_table_names_return = sqlite_plugins.get_sqlite_table_names('tests/test.sqlite')

        self.expected_data = ['test1', 'test2']

        self.assertEqual(self.sqlite_table_names_return, self.expected_data)

    def test_sqliteGetTableRows(self):
        self.sqlite_table_rows_return = sqlite_plugins.read_sqlite_table('tests/test.sqlite', 'test1')

        self.expected_data = [(u'1', u'Dan', u'33'), (u'2', u'Jon', u'23')]

        self.assertEqual(self.sqlite_table_rows_return, self.expected_data)

    def test_sqliteGetTablesRows(self):
        self.sqlite_tables_rows_return = sqlite_plugins.read_sqlite_tables('tests/test.sqlite')

        self.expected_data = {u'test1': [(u'1', u'Dan', u'33'), (u'2', u'Jon', u'23')], u'test2': [(u'1',
                                                                                                    u'New York City',
                                                                                                    u'NY'),
                                                                                                      (u'2',
                                                                                                    u'Portland',
                                                                                                    u'OR')]}

        self.assertEqual(self.sqlite_tables_rows_return, self.expected_data)

if __name__ == '__main__':
    # TODO: Add sqlite views test
    # TODO: Add csv writer test

    unittest.main()


