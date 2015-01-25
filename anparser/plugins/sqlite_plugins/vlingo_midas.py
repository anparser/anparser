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


def vlingo_midas(file_list):
    """
    Parses contactsManager.db database from com.vlingo.midas

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: data
    vlingo_database = None
    data_data = None

    for file_path in file_list:
        if file_path.endswith('contactsManager.db'):
            vlingo_database = file_path
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'data' in tables:
                try:
                    data_data = __init__.read_sqlite_table(
                        file_path, 'data',
                        columns='_id, raw_contact_id, contact_id, times_contacted, starred, display_name, '
                                'lookup')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    vlingo_contacts_list = []
    vlingo_data = OrderedDict()

    # Add tables from contactsManager.db to vlingo_contacts_list
    # Add data from data table to vlingo_data
    if data_data:
        for entry in data_data:
            vlingo_data['Database'] = vlingo_database
            vlingo_data['Table'] = 'data'
            vlingo_data['Data Id'] = entry[0]
            vlingo_data['Raw Contact Id'] = entry[1]
            vlingo_data['Contact Id'] = entry[2]
            vlingo_data['Display Name'] = entry[5]
            vlingo_data['Times Contacted'] = entry[3]
            vlingo_data['Starred'] = entry[4]
            vlingo_data['Lookup'] = entry[6]

            vlingo_contacts_list.append(vlingo_data)
            vlingo_data = OrderedDict()

    return vlingo_contacts_list