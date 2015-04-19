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
__date__ = '20150107'
__version__ = '0.00'

from ingest import sqlite_processor, time_processor


def android_browser(file_list):
    """
    Parses browser database from com.android.browser

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # TODO: Add in support for other tables (images, thumbnails).
    # Initialize table variables: bookmarks, history, v_accounts
    bookmarks_data = None
    history_data = None

    for file_path in file_list:
        if file_path.endswith(u'browser2.db'):
            tables =  sqlite_processor.get_sqlite_table_names(file_path)
            if u'bookmarks' in tables:
                bookmarks_data = sqlite_processor.read_sqlite_table(
                    file_path, u'bookmarks', u'_id, title, url, deleted, created, modified')
                if bookmarks_data is not None:
                    bookmarks_data.created = time_processor.unix_time(bookmarks_data.created)
                    bookmarks_data.modified = time_processor.unix_time(bookmarks_data.modified)
                    bookmarks_data['Database Path'] = file_path

            if u'history' in tables:
                history_data = sqlite_processor.read_sqlite_table(
                    file_path, u'history', u'_id, title, url, date, visits')
                if history_data is not None:
                    history_data.date = time_processor.unix_time(history_data.date)
                    history_data['Database Path'] = file_path

    return bookmarks_data, history_data