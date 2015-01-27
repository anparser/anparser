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
            vending_data['Library Id'] = entry['library_id']
            vending_data['Doc Id'] = entry['doc_id']
            vending_data['Account'] = entry['account']
            vending_data['Document Hash'] = entry['document_hash']
            vending_data['App Certificate Hash'] = entry['app_certificate_hash']

            vending_library_list.append(vending_data)
            vending_data = OrderedDict()

    # Add data from localappstate.db database to vending_localapp_list
    # Add data from appstate table to vending_data
    if localapp_data:
        for entry in localapp_data:
            vending_data['Database'] = localapp_database
            vending_data['Table'] = 'appstate'
            try:
                vending_data['Title'] = entry['title'].encode('utf-8')
            except AttributeError:
                vending_data['Title'] = entry['title']
            try:
                vending_data['Package Name'] = entry['package_name'].encode('utf-8')
            except AttributeError:
                vending_data['Package Name'] = entry['package_name']
            vending_data['Account'] = entry['account']
            try:
                vending_data['First Download'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['first_download_ms'] / 1000.))
            except TypeError:
                vending_data['First Download'] = ''
            vending_data['Auto Update'] = entry['auto_update']
            try:
                vending_data['Last Update'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['last_update_timestamp_ms'] / 1000.))
            except TypeError:
                vending_data['Last Update'] = ''
            vending_data['Last Notified Version'] = entry['last_notified_version']
            vending_data['Desired Version'] = entry['desired_version']
            try:
                vending_data['Download Uri'] = entry['download_uri'].encode('utf-8')
            except AttributeError:
                vending_data['Download Uri'] = entry['download_uri']

            vending_localapp_list.append(vending_data)
            vending_data = OrderedDict()

    # Add data from suggestions.db database to vending_suggestions_list
    # Add data from suggestions table to vending_data
    if suggestions_data:
        for entry in suggestions_data:
            vending_data['Database'] = suggestions_database
            vending_data['Table'] = 'suggestions'
            vending_data['Id'] = entry['_id']
            vending_data['Display'] = entry['display1']
            vending_data['Query'] = entry['query']
            try:
                vending_data['Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['date'] / 1000.))
            except TypeError:
                vending_data['Date'] = ''

            vending_suggestions_list.append(vending_data)
            vending_data = OrderedDict()

    return vending_library_list, vending_localapp_list, vending_suggestions_list