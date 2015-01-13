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
__date__ = '20150113'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import time


def android_mms(file_list):
    """
    Parses message_glance database from com.android.mms

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # Initialize table variables: events, logs
    events_data = None
    logs_data = None

    for file_path in file_list:
        if file_path.endswith('message_glance.db'):
            tables = __init__.get_sqlite_table_names(file_path)
            if 'events' in tables:
                try:
                    events_data = __init__.read_sqlite_table(
                        file_path, 'events',
                        columns='_id, address, deleted, eventDate')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'logs' in tables:
                try:
                    logs_data = __init__.read_sqlite_table(
                        file_path, 'logs',
                        columns='_id, address, deleted, incoming, outgoing')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    mms_data_list = []
    mms_data = OrderedDict()

    # Add data from message_glance.db to mms_data_list
    # Add data from events table to mms_data
    if events_data:
        for entry in events_data:
            mms_data['Table'] = 'events'
            mms_data['event id'] = entry[0]
            mms_data['log id'] = ''
            mms_data['address'] = entry[1]
            mms_data['deleted'] = entry[2]
            try:
                mms_data['event date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except (TypeError, ValueError):
                mms_data['event date'] = ''
            mms_data['incoming'] = ''
            mms_data['outgoing'] = ''

            mms_data_list.append(mms_data)
            mms_data = OrderedDict()

    # Add data from logs table to mms_data
    if logs_data:
        for entry in logs_data:
            mms_data['Table'] = 'logs'
            mms_data['event id'] = ''
            mms_data['log id'] = entry[0]
            mms_data['address'] = entry[1]
            mms_data['deleted'] = entry[2]
            mms_data['event date'] = ''
            mms_data['incoming'] = entry[3]
            mms_data['outgoing'] = entry[4]

            mms_data_list.append(mms_data)
            mms_data = OrderedDict()

    return mms_data_list