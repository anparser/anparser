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
__date__ = '20150119'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import time


def kik_android(file_list):
    """
    Parses kikDatabase.db database from kik.android

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: KIKContentTable, KIKcontactsTable, messagesTable
    kik_database = None
    content_data = None
    contacts_data = None
    messages_data = None

    for file_path in file_list:
        if file_path.endswith('kikDatabase.db'):
            kik_database = file_path
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'KIKContentTable' in tables:
                try:
                    content_data = __init__.read_sqlite_table(
                        file_path, 'KIKContentTable',
                        columns='_id, content_id, content_type, content_name, content_string')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'KIKcontactsTable' in tables:
                try:
                    contacts_data = __init__.read_sqlite_table(
                        file_path, 'KIKcontactsTable',
                        columns='_id, jid, display_name, user_name, is_blocked, '
                                'is_ignored')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'messagesTable' in tables:
                try:
                    messages_data = __init__.read_sqlite_table(
                        file_path, 'messagesTable',
                        columns='_id, body, partner_jid, was_me, read_state, uid, '
                                'length, timestamp, content_id, app_id')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    kik_contacts_list = []
    kik_chat_list = []
    kik_data = OrderedDict()

    # Add tables from kikDatabase.db to kik_contacts_list
    # Add data from KIKcontactsTable table to kik_data
    if contacts_data:
        for entry in contacts_data:
            kik_data['Database'] = kik_database
            kik_data['Table'] = 'KIKcontactsTable'
            kik_data['Id'] = entry[0]
            kik_data['Jid'] = entry[1]
            kik_data['Display Name'] = entry[2]
            kik_data['User Name'] = entry[3]
            kik_data['Is Blocked'] = entry[4]
            kik_data['Is Ignored'] = entry[5]

            kik_contacts_list.append(kik_data)
            kik_data = OrderedDict()

    # Add data from kikDatabase.db to kik_chat_list
    # Add data from KIKContentTable table to kik_data
    if content_data:
        for entry in content_data:
            kik_data['Database'] = kik_database
            kik_data['Table'] = 'KIKContentTable'
            kik_data['App Id'] = ''
            kik_data['KIKContentTable Id'] = entry[0]
            kik_data['Content Id'] = entry[1]
            kik_data['Message Id'] = ''
            kik_data['Body'] = ''
            kik_data['Length'] = ''
            kik_data['Partner Jid'] = ''
            kik_data['Was Me'] = ''
            kik_data['Read State'] = ''
            kik_data['Uid'] = ''
            kik_data['Timestamp'] = ''
            kik_data['Content Type'] = entry[2]
            kik_data['Content Name'] = entry[3]
            kik_data['Content String'] = entry[4]

            kik_chat_list.append(kik_data)
            kik_data = OrderedDict()

    # Add data from messagesTable table to kik_data
    if messages_data:
        for entry in messages_data:
            kik_data['Database'] = kik_database
            kik_data['Table'] = 'messagesTable'
            kik_data['App Id'] = entry[9]
            kik_data['KIKContentTable Id'] = ''
            kik_data['Content Id'] = entry[8]
            kik_data['Message Id'] = entry[0]
            kik_data['Body'] = entry[1]
            kik_data['Length'] = entry[6]
            kik_data['Partner Jid'] = entry[2]
            kik_data['Was Me'] = entry[3]
            kik_data['Read State'] = entry[4]
            kik_data['Uid'] = entry[5]
            try:
                kik_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[7] / 1000.))
            except TypeError:
                kik_data['Timestamp'] = ''
            kik_data['Content Type'] = ''
            kik_data['Content Name'] = ''
            kik_data['Content String'] = ''

            kik_chat_list.append(kik_data)
            kik_data = OrderedDict()

    return kik_contacts_list, kik_chat_list