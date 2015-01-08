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

from collections import OrderedDict
import logging
import sqlite_plugins
import time


def android_downloads(file_list):
    """
    Parses downloads database from com.android.providers.database

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variable: downloads
    download_data = None

    for file_path in file_list:
        if file_path.endswith('downloads.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'downloads' in tables:
                try:
                    download_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'downloads',
                        columns='_id, title, description, mimetype, lastmod, uid, '
                                'etag, uri, hint, _data, total_bytes, mediaprovider_uri')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    downloads_data_list = []
    downloads_data = OrderedDict()

    # Add data from downloads table to downloads_data
    if download_data:
        for entry in download_data:
            downloads_data['Table'] = 'downloads'
            downloads_data['id'] = entry[0]
            downloads_data['title'] = entry[1]
            downloads_data['description'] = entry[2]
            downloads_data['mimetype'] = entry[3]
            try:
                downloads_data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.))
            except TypeError:
                downloads_data['modified'] = ''
            downloads_data['uid'] = entry[5]
            downloads_data['etag'] = entry[6]
            downloads_data['uri'] = entry[7]
            downloads_data['hint'] = entry[8]
            downloads_data['data'] = entry[9]
            downloads_data['total bytes'] = entry[10]
            downloads_data['mediaprovider_uri'] = entry[11]

            downloads_data_list.append(downloads_data)
            downloads_data = OrderedDict()


    return downloads_data_list