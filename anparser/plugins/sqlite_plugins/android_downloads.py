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
__date__ = '20150108'
__version__ = '0.00'

import time

from ingest import sqlite_processor, time_processor
import logging

def android_downloads(file_list):
    """
    Parses downloads database from com.android.providers.database

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variable: downloads
    download_data = None

    for file_path in file_list:
        if file_path.endswith(u'downloads.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'downloads' in tables:
                download_data = sqlite_processor.read_sqlite_table(
                    file_path, u'downloads', u'_id, title, description, mimetype, deleted, lastmod, uid, '
                                             u'etag, uri, hint, _data, total_bytes, mediaprovider_uri')
                try:
                    download_data.lastmod = time_processor.unix_time(download_data.lastmod)
                    download_data['Database Path'] = file_path
                except AttributeError as e:
                    logging.error(AttributeError(e))

    return download_data