# -*- coding: utf-8 -*-
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

__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '20150102'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import time


def android_contacts(file_list):
    """
    Parse data specifically from the Android Contacts Database file

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize Variable
    contacts_database = None
    raw_contacts_data = None
    accounts_data = None
    phone_lookup_data = None

    for file_path in file_list:
        if file_path.endswith('contacts2.db'):
            contacts_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'raw_contacts' in tables:
                try:
                    raw_contacts_data = __init__.read_sqlite_table(
                        file_path, 'raw_contacts', columns='contact_id, display_name, modified_time')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'accounts' in tables:
                try:
                    accounts_data = __init__.read_sqlite_table(file_path, 'accounts',
                                                                     columns='_id, account_name, account_type')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'phone_lookup' in tables:
                try:
                    phone_lookup_data = __init__.read_sqlite_table(file_path, 'phone_lookup',
                                                                         columns='raw_contact_id, normalized_number')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))

    contact_data_list = []
    contact_data = OrderedDict()

    if raw_contacts_data:
        for entry in raw_contacts_data:
            contact_data['Database'] = contacts_database
            contact_data['Contact Id'] = entry[0]
            contact_data['Display Name'] = entry[1]
            try:
                contact_data['Modified Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.0))
            except TypeError:
                contact_data['Modified Time'] = ''
            for item in phone_lookup_data:
                if item[0] == entry[0]:
                    contact_data['Normalized Number'] = item[1]
            contact_data_list.append(contact_data)
            contact_data = OrderedDict()

    return contact_data_list