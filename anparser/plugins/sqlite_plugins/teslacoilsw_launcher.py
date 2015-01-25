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
import time


def teslacoilsw_launcher(file_list):
    """
    Parses launcher.db database from com.teslacoilsw.launcher

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: allapps, favorites
    tesla_database = None
    allapps_data = None
    favorites_data = None

    for file_path in file_list:
        if file_path.endswith('launcher.db') and file_path.count('com.teslacoilsw.launcher') > 0:
            tesla_database = file_path
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'allapps' in tables:
                try:
                    allapps_data = __init__.read_sqlite_table(
                        file_path, 'allapps',
                        columns='componentName, title, lastUpdateTime')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'favorites' in tables:
                try:
                    favorites_data = __init__.read_sqlite_table(
                        file_path, 'favorites',
                        columns='_id, title, intent')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    tesla_favorites_list = []
    tesla_allapps_list = []
    tesla_data = OrderedDict()

    # Add tables from launcher.db to tesla_favorites_list
    # Add data from favorites table to tesla_data
    if favorites_data:
        for entry in favorites_data:
            tesla_data['Database'] = tesla_database
            tesla_data['Table'] = 'favorites'
            tesla_data['Favorites Id'] = entry[0]
            tesla_data['Title'] = entry[1]
            tesla_data['Intent'] = entry[2]

            tesla_favorites_list.append(tesla_data)
            tesla_data = OrderedDict()

    # Add data from allapps table to tesla_data
    if allapps_data:
        for entry in allapps_data:
            tesla_data['Database'] = tesla_database
            tesla_data['Table'] = 'allapps'
            tesla_data['Component Name'] = entry[0]
            tesla_data['Title'] = entry[1]
            try:
                tesla_data['Last Update Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.))
            except TypeError:
                tesla_data['Last Update Time'] = ''

            tesla_allapps_list.append(tesla_data)
            tesla_data = OrderedDict()

    return tesla_allapps_list, tesla_favorites_list