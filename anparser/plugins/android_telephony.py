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
import sqlite_plugins
import time


def read_sms(db_data):

    data_dict_list = []
    data_dict = OrderedDict()

    for entry in db_data:
        data_dict['id'] = entry[0]
        data_dict['thread_id'] = entry[1]
        data_dict['address'] = entry[2]
        data_dict['person'] = entry[3]
        try:
            data_dict['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.0))
        except TypeError:
            data_dict['date'] = ''
        try:
            data_dict['date_sent'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.0))
        except TypeError:
            data_dict['date_sent'] = ''
        data_dict['body'] = entry[6]
        data_dict['read'] = entry[7]
        data_dict['seen'] = entry[8]
        data_dict_list.append(data_dict)
        data_dict = OrderedDict()

    return data_dict_list


def read_sms_threads(db_data):

    data_dict_list = []
    data_dict = OrderedDict()

    for entry in db_data:
        data_dict['id'] = entry[0]
        try:
            data_dict['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[1] / 1000.0))
        except TypeError:
            data_dict['date'] = ''
        data_dict['message_count'] = entry[2]
        data_dict['snippet'] = entry[3]
        data_dict['read'] = entry[4]
        data_dict['has_attachment'] = entry[5]
        data_dict_list.append(data_dict)
        data_dict = OrderedDict()

    return data_dict_list


def android_telephony(file_listing):

    sms_data = None
    threads_data = None
    parsed_sms_data = None
    parsed_threads_data = None

    for file_path in file_listing:
        if file_path.endswith('mmssms.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'sms' in tables:
                try:
                    sms_data = sqlite_plugins.read_sqlite_table(file_path, 'sms',
                                                                columns='_id, thread_id, address, person, date, '
                                                                        'date_sent, body, read, seen')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
                if sms_data:
                    parsed_sms_data = read_sms(sms_data)

            if 'threads' in tables:
                try:
                    threads_data = sqlite_plugins.read_sqlite_table(file_path, 'threads',
                                                                    columns='_id, date, message_count, snippet, read, '
                                                                            'has_attachment')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
                if threads_data:
                    parsed_threads_data = read_sms_threads(threads_data)


    return parsed_sms_data, parsed_threads_data