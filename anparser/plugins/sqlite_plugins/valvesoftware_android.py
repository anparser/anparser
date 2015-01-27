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
__date__ = '20150124'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import time


def valvesoftware_android(file_list):
    """
    Parses databases from com.valvesoftware.android.steam.community

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: debug, message
    debug_database = None
    message_database = None
    debug_data = None
    message_data = None
    friends_data = None

    for file_path in file_list:
        if file_path.endswith('dbgutil.db'):
            debug_database = file_path
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'dbgutil' in tables:
                try:
                    debug_data = __init__.read_sqlite_table(
                        file_path, 'dbgutil',
                        columns='_id, msgtime, key, value')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('umqcomm.db'):
            message_database = file_path
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []
            if 'UmqInfo' in tables:
                try:
                    friends_data = __init__.read_sqlite_table(
                        file_path, 'UmqInfo',
                        columns='id1, id2, name')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'UmqMsg' in tables:
                try:
                    message_data = __init__.read_sqlite_table(
                        file_path, 'UmqMsg',
                        columns='_id, myuser1, myuser2, wuser1, wuser2, msgincoming, msgunread, '
                                'msgtime, msgtype, bindata')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    valve_friends_list = []
    valve_chat_list = []
    valve_debug_list = []
    valve_data = OrderedDict()

    # Add tables from dbgutil.db to valve_debug_list
    # Add data from dbgutil table to valve_data
    if debug_data:
        for entry in debug_data:
            valve_data['Database'] = debug_database
            valve_data['Table'] = 'dbgutil'
            valve_data['Id'] = entry['_id']
            try:
                valve_data['Message Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['msgtime']))
            except TypeError:
                valve_data['Message Time'] = ''
            valve_data['Key'] = entry['key']
            valve_data['Value'] = entry['value']

            valve_debug_list.append(valve_data)
            valve_data = OrderedDict()

    # Add data from umqcomm.db to valve_friends_list
    # Add data from UmqInfo table to valve_data
    if friends_data:
        for entry in friends_data:
            valve_data['Database'] = message_database
            valve_data['Table'] = 'UmqInfo'
            valve_data['Id 1'] = entry['id1']
            valve_data['Id 2'] = entry['id2']
            valve_data['Name'] = entry['name']

            valve_friends_list.append(valve_data)
            valve_data = OrderedDict()

    # Add data from umqcomm.db to valve_message_list
    # Add data from UmqMsg table to valve_data
    if message_data:
        for entry in message_data:
            valve_data['Database'] = message_database
            valve_data['Table'] = 'UmqMsg'
            valve_data['Id'] = entry['_id']
            valve_data['My User 1'] = entry['myuser1']
            valve_data['My User 2'] = entry['myuser2']
            valve_data['W User 1'] = entry['wuser1']
            valve_data['W User 2'] = entry['wuser2']
            valve_data['Message Incoming'] = entry['msgincoming']
            valve_data['Message Unread'] = entry['msgunread']
            try:
                valve_data['Message Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['msgtime']))
            except TypeError:
                valve_data['Message Time'] = ''
            valve_data['Message Type'] = entry['msgtype']
            valve_data['Data'] = entry['bindata']

            valve_chat_list.append(valve_data)
            valve_data = OrderedDict()

    return valve_friends_list, valve_chat_list, valve_debug_list,