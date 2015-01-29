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

from collections import OrderedDict
import logging
import __init__


def android_emergencymode(file_list):
    """
    Parses emergency.db database from com.sec.android.provider.emergencymode

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variable: ecc
    emergency_database = None
    preference_data = None

    for file_path in file_list:
        if file_path.endswith('emergency.db'):
            emergency_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'prefsettings' in tables:
                try:
                    preference_data = __init__.read_sqlite_table(
                        file_path, 'prefsettings',
                        columns='pref, value')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    emergency_data_list = []
    emergency_data = OrderedDict()

    # Add data from prefsettings table to emergency_data
    if preference_data:
        for entry in preference_data:
            emergency_data['Database'] = emergency_database
            emergency_data['Table'] = 'prefsettings'
            emergency_data['Preference'] = entry['pref']
            emergency_data['Value'] = entry['value']

            emergency_data_list.append(emergency_data)
            emergency_data = OrderedDict()


    return emergency_data_list