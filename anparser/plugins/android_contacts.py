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

import sqlite_plugins
import time


def android_contacts(file_list):
    """
    Parse data specifically from the Android Contacts Database file

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize Variable
    raw_contacts_data = None
    accounts_data = None
    phone_lookup_data = None

    for file_path in file_list:
        if file_path.endswith('contacts2.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'raw_contacts' in tables:
                raw_contacts_data = sqlite_plugins.read_sqlite_table(file_path, 'raw_contacts',
                                                                     columns='contact_id, display_name, modified_time')
            if 'accounts' in tables:
                accounts_data = sqlite_plugins.read_sqlite_table(file_path, 'accounts',
                                                                 columns='_id, account_name, account_type')
            if 'phone_lookup' in tables:
                phone_lookup_data = sqlite_plugins.read_sqlite_table(file_path, 'phone_lookup',
                                                                     columns='raw_contact_id, normalized_number')

    contact_data_list = []
    contact_data = dict()

    if raw_contacts_data:
        for entry in raw_contacts_data:
            contact_data['contact_id'] = entry[0]
            contact_data['display_name'] = entry[1]
            contact_data['modified_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.0))
            for item in phone_lookup_data:
                if item[0] == entry[0]:
                    contact_data['normalized_number'] = item[1]
            contact_data_list.append(contact_data)
            contact_data = dict()

    return contact_data_list