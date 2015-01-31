# -*- coding: utf-8 -*-
"""
anparser - an Open Source Android Artifact Parser
Copyright (C) 2015  Preston Miller

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

__author__ = 'prmiller91'
__license__ = 'GPLv3'
__date__ = '20150125'
__version__ = '0.00'

import logging
import sqlite_processor


def vlingo_midas(file_list):
    """
    Parses contactsManager.db database from com.vlingo.midas

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: data
    data_data = None

    for file_path in file_list:
        if file_path.endswith(u'contactsManager.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'data' in tables:
                data_data = sqlite_processor.read_sqlite_table(
                    file_path, u'data',
                    u'_id, raw_contact_id, contact_id, times_contacted, starred, display_name, '
                    u'lookup')

    return data_data