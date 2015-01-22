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
__date__ = '20150109'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import time


def android_vending(file_list):
    """
    Parses database folder from com.android.vending

    :param file_list: List of all files
    :return: Dictionary of parsed data from databases
    """
    # Initialize table variables: library, localappstate, suggestions
    library_database = None
    localapp_database = None
    suggestions_database = None
    library_data = None
    localapp_data = None
    suggestions_data = None

    for file_path in file_list:
        if file_path.endswith('library.db'):
            library_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'ownership' in tables:
                try:
                    library_data = __init__.read_sqlite_table(
                        file_path, 'ownership',
                        columns='account, library_id, doc_id, document_hash, '
                                'app_certificate_hash')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('localappstate.db'):
            localapp_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'appstate' in tables:
                try:
                    localapp_data = __init__.read_sqlite_table(
                        file_path, 'appstate',
                        columns='package_name, auto_update, desired_version, download_uri, '
                                'first_download_ms, account, title, last_notified_version, '
                                'last_update_timestamp_ms')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('suggestions.db'):
            suggestions_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'suggestions' in tables:
                try:
                    suggestions_data = __init__.read_sqlite_table(
                        file_path, 'suggestions',
                        columns='_id, display1, query, date')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    vending_library_list = []
    vending_localapp_list = []
    vending_suggestions_list = []
    vending_data = OrderedDict()

    # Add data from library.db database to vending_library_list
    # Add data from ownership table to vending_data
    if library_data:
        for entry in library_data:
            vending_data['Database'] = library_database
            vending_data['Table'] = 'ownership'
            vending_data['Library Id'] = entry[1]
            vending_data['Doc Id'] = entry[2]
            vending_data['Account'] = entry[0]
            vending_data['Document Hash'] = entry[3]
            vending_data['App Certificate Hash'] = entry[4]

            vending_library_list.append(vending_data)
            vending_data = OrderedDict()

    # Add data from localappstate.db database to vending_localapp_list
    # Add data from appstate table to vending_data
    if localapp_data:
        for entry in localapp_data:
            vending_data['Database'] = localapp_database
            vending_data['Table'] = 'appstate'
            try:
                vending_data['Title'] = entry[6].encode('utf-8')
            except AttributeError:
                vending_data['Title'] = entry[6]
            try:
                vending_data['Package Name'] = entry[0].encode('utf-8')
            except AttributeError:
                vending_data['Package Name'] = entry[0]
            vending_data['Account'] = entry[5]
            try:
                vending_data['First Download'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.))
            except TypeError:
                vending_data['First Download'] = ''
            vending_data['Auto Update'] = entry[1]
            try:
                vending_data['Last Update'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[8] / 1000.))
            except TypeError:
                vending_data['Last Update'] = ''
            vending_data['Last Notified Version'] = entry[7]
            vending_data['Desired Version'] = entry[2]
            try:
                vending_data['Download Uri'] = entry[3].encode('utf-8')
            except AttributeError:
                vending_data['Download Uri'] = entry[3]

            vending_localapp_list.append(vending_data)
            vending_data = OrderedDict()

    # Add data from suggestions.db database to vending_suggestions_list
    # Add data from suggestions table to vending_data
    if suggestions_data:
        for entry in suggestions_data:
            vending_data['Database'] = suggestions_database
            vending_data['Table'] = 'suggestions'
            vending_data['Id'] = entry[0]
            vending_data['Display'] = entry[1]
            vending_data['Query'] = entry[2]
            try:
                vending_data['Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                vending_data['Date'] = ''

            vending_suggestions_list.append(vending_data)
            vending_data = OrderedDict()

    return vending_library_list, vending_localapp_list, vending_suggestions_list