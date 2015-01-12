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
import sqlite_plugins
import time


def android_vending(file_list):
    """
    Parses database folder from com.android.vending

    :param file_list: List of all files
    :return: Dictionary of parsed data from databases
    """
    # Initialize table variables: library, localappstate, suggestions
    library_data = None
    localapp_data = None
    suggestions_data = None

    for file_path in file_list:
        if file_path.endswith('library.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'ownership' in tables:
                try:
                    library_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'ownership',
                        columns='account, library_id, doc_id, document_hash, '
                                'app_certificate_hash')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('localappstate.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'appstate' in tables:
                try:
                    localapp_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'appstate',
                        columns='package_name, auto_update, desired_version, download_uri, '
                                'first_download_ms, account, title, last_notified_version, '
                                'last_update_timestamp_ms')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('suggestions.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'suggestions' in tables:
                try:
                    suggestions_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'suggestions',
                        columns='_id, display1, query, date')
                except sqlite_plugins.sqlite3.OperationalError as exception:
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
            vending_data['Table'] = 'ownership'
            vending_data['library id'] = entry[1]
            vending_data['doc id'] = entry[2]
            vending_data['account'] = entry[0]
            vending_data['document hash'] = entry[3]
            vending_data['app certificate hash'] = entry[4]

            vending_library_list.append(vending_data)
            vending_data = OrderedDict()

    # Add data from localappstate.db database to vending_localapp_list
    # Add data from appstate table to vending_data
    if localapp_data:
        for entry in localapp_data:
            vending_data['Table'] = 'appstate'
            vending_data['title'] = entry[6]
            vending_data['package name'] = entry[0]
            vending_data['account'] = entry[5]
            try:
                vending_data['first download'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.))
            except TypeError:
                vending_data['first download'] = ''
            vending_data['auto update'] = entry[1]
            try:
                vending_data['last update'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[8] / 1000.))
            except TypeError:
                vending_data['last update'] = ''
            vending_data['last_notified_version'] = entry[7]
            vending_data['desired version'] = entry[2]
            vending_data['download uri'] = entry[3]

            vending_localapp_list.append(vending_data)
            vending_data = OrderedDict()

    # Add data from suggestions.db database to vending_suggestions_list
    # Add data from suggestions table to vending_data
    if suggestions_data:
        for entry in suggestions_data:
            vending_data['Table'] = 'suggestions'
            vending_data['id'] = entry[0]
            vending_data['display'] = entry[1]
            vending_data['query'] = entry[2]
            try:
                vending_data['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                vending_data['date'] = ''

            vending_suggestions_list.append(vending_data)
            vending_data = OrderedDict()

    return vending_library_list, vending_localapp_list, vending_suggestions_list