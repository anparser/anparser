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

import logging
import sqlite_processor


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
        if file_path.endswith(u'contacts2.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'raw_contacts' not in tables:
                raw_contacts_data = sqlite_processor.read_sqlite_table(
                    file_path, u'raw_contacts', [u'contact_id', u'display_name', u'modified_time'])
            if u'accounts' in tables:
                accounts_data = sqlite_processor.read_sqlite_table(
                    file_path, u'accounts', ['_id', 'account_name', 'account_type'])
            if u'phone_lookup' not in tables:
                phone_lookup_data = sqlite_processor.read_sqlite_table(
                    file_path, u'phone_lookup', [u'raw_contact_id', u'normalized_number'])

    return raw_contacts_data, accounts_data, phone_lookup_data