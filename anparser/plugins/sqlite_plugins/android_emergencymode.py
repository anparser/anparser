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

from ingest import sqlite_processor


def android_emergencymode(file_list):
    """
    Parses emergency.db database from com.sec.android.provider.emergencymode

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variable: ecc
    preference_data = None

    for file_path in file_list:
        if file_path.endswith(u'emergency.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'prefsettings' in tables:
                preference_data = sqlite_processor.read_sqlite_table(
                    file_path, u'prefsettings', u'pref, value')
                if preference_data is not None:
                    preference_data['Database Path'] = file_path

    return preference_data