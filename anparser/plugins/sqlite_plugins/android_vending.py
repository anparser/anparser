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

from ingest import sqlite_processor  # , time_processor


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
        if file_path.endswith(u'library.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'ownership' in tables:
                library_data = sqlite_processor.read_sqlite_table(
                    file_path, u'ownership', u'account, library_id, doc_id, document_hash, app_certificate_hash')

        if file_path.endswith(u'localappstate.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'appstate' in tables:
                localapp_data = sqlite_processor.read_sqlite_table(
                    file_path, u'appstate', u'package_name, auto_update, desired_version, download_uri, '
                                             u'first_download_ms, account, title, last_notified_version, '
                                             u'last_update_timestamp_ms')
                if localapp_data is not None:
                    localapp_data.first_download_ms = time_processor.unix_time(localapp_data.first_download_ms)
                    localapp_data.last_update_timestamp_ms = time_processor.unix_time(
                        localapp_data.last_update_timestamp_ms)

        if file_path.endswith(u'suggestions.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'suggestions' in tables:
                suggestions_data = sqlite_processor.read_sqlite_table(
                    file_path, u'suggestions', u'_id, display1, query, date')
                if suggestions_data is not None:
                    suggestions_data.date = time_processor.unix_time(suggestions_data.date)

    return library_data, localapp_data, suggestions_data