# -*- coding: utf-8 -*-

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

from ingest import xml_processor
from ingest import sqlite_processor
from pandas.util.testing import assert_frame_equal
import pandas as pd

class TestAnParser(unittest.TestCase):

    def setUp(self):
        pass

    def test_xmlFiles(self):
        self.xml_return = xml_processor.parse_xml_file_notree('anparser/tests/test.xml')

        self.expected_data = [{'name': 'ds__downloads_json__',
                          'text_entry': '[{"minVersion":0,"filename":"libAppDataSearchExt_armeabi_v7a.so",'
                                        '"sizeBytes":3810616}]'},
                         {'name': 'libAppDataSearchExt_armeabi_v7a.so__dest__', 'text_entry': 'None'},
                         {'name': 'ds__next_alarm__', 'value': '178309873', 'text_entry': 'None'}]

        self.assertEqual(self.xml_return, self.expected_data)

    def test_sqliteGetTableNames(self):
        self.sqlite_table_names_return = sqlite_processor.get_sqlite_table_names('anparser/tests/test.sqlite')

        self.expected_data = [u'test1', u'test2']

        self.assertEqual(self.sqlite_table_names_return, self.expected_data)

    def test_sqliteGetTableRows(self):
        self.sqlite_table_rows_return = sqlite_processor.read_sqlite_table('anparser/tests/test.sqlite', 'test1')

        self.expected_data = pd.DataFrame([{'age': u'33', 'id':u'1', 'name':u'Dan'},
                                          {'age':u'23', 'id':u'2', 'name':u'Jon'}])

        assert_frame_equal(self.sqlite_table_rows_return.sort(axis=1), self.expected_data.sort(axis=1))


    def test_sqliteGetTablesRows(self):
        self.sqlite_tables_rows_return = sqlite_processor.read_sqlite_tables('anparser/tests/test.sqlite')

        self.expected_data = {u'test1': pd.DataFrame([{'age': u'33', 'id':u'1', 'name':u'Dan'},
                                         {'age':u'23', 'id':u'2', 'name':u'Jon'}]),
                              u'test2': pd.DataFrame([{'city':u'New York City', 'state':u'NY', 'id':u'1'},
                                          {'city':u'Portland', 'state':u'OR', 'id':u'2'}])}

        for (f1, f2) in zip(self.sqlite_tables_rows_return.values(), self.expected_data.values()):
            assert_frame_equal(f1.sort(axis=1), f2.sort(axis=1))

if __name__ == '__main__':
    # TODO: Add sqlite views test
    # TODO: Add csv writer test

    unittest.main()