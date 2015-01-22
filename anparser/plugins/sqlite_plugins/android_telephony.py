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


def read_sms(db_data, db_path):

    data_dict_list = []
    data_dict = OrderedDict()

    for entry in db_data:
        data_dict['Database'] = db_path
        data_dict['Table'] = 'sms'
        data_dict['Id'] = entry[0]
        data_dict['Thread Id'] = entry[1]
        data_dict['Address'] = entry[2]
        data_dict['Person'] = entry[3]
        try:
            data_dict['Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.0))
        except TypeError:
            data_dict['Date'] = ''
        try:
            data_dict['Date_Sent'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.0))
        except TypeError:
            data_dict['Date_Sent'] = ''
        data_dict['Body'] = entry[6]
        data_dict['Read'] = entry[7]
        data_dict['Seen'] = entry[8]
        data_dict_list.append(data_dict)
        data_dict = OrderedDict()

    return data_dict_list


def read_sms_threads(db_data, db_path):

    data_dict_list = []
    data_dict = OrderedDict()

    for entry in db_data:
        data_dict['Database'] = db_path
        data_dict['Table'] = 'threads'
        data_dict['Id'] = entry[0]
        try:
            data_dict['Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[1] / 1000.0))
        except TypeError:
            data_dict['Date'] = ''
        data_dict['Message Count'] = entry[2]
        data_dict['Snippet'] = entry[3]
        data_dict['Read'] = entry[4]
        data_dict['Has Attachment'] = entry[5]
        data_dict_list.append(data_dict)
        data_dict = OrderedDict()

    return data_dict_list


def android_telephony(file_listing):

    mmssms_database = None
    sms_data = None
    threads_data = None
    parsed_sms_data = None
    parsed_threads_data = None

    for file_path in file_listing:
        if file_path.endswith('mmssms.db'):
            mmssms_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'sms' in tables:
                try:
                    sms_data = __init__.read_sqlite_table(file_path, 'sms',
                                                                columns='_id, thread_id, address, person, date, '
                                                                        'date_sent, body, read, seen')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
                if sms_data:
                    parsed_sms_data = read_sms(sms_data, mmssms_database)

            if 'threads' in tables:
                try:
                    threads_data = __init__.read_sqlite_table(file_path, 'threads',
                                                                    columns='_id, date, message_count, snippet, read, '
                                                                            'has_attachment')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
                if threads_data:
                    parsed_threads_data = read_sms_threads(threads_data, mmssms_database)


    return parsed_sms_data, parsed_threads_data