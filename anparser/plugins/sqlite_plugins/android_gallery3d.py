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
__date__ = '20150114'
__version__ = '0.00'

from collections import OrderedDict
import logging
import sqlite_processor


def android_gallery3d(file_list):
    """
    Parses databases from com.android.gallery3d

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # Initialize table variables: file_info, download, albums, photos, users
    file_database = None
    download_database = None
    picasa_database = None
    file_info_data = None
    download_data = None
    albums_data = None
    photos_data = None
    users_data = None

    for file_path in file_list:
        if file_path.endswith(u'FileInfo.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'file_info' in tables:
                file_info_data = sqlite_processor.read_sqlite_table(
                    file_path, u'file_info', [u'hash_key', u'file_path', u'file_info_type'])

        if file_path.endswith(u'download.db') and file_path.count(u'gallery3d') > 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'download' in tables:
                download_data = sqlite_processor.read_sqlite_table(
                    file_path, u'download', [u'_id', u'_data', u'content_url', u'hash_code', u'last_access',
                                             u'last_updated', u'_size'])

        if file_path.endswith(u'picasa.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'albums' in tables:
                albums_data = sqlite_processor.read_sqlite_table(
                    file_path, u'albums', [u'_id', u'bytes_used', u'date_edited', u'date_published', u'date_updated',
                                           u'html_page_url', u'location_string', u'num_photos', u'summary',
                                           u'sync_account', u'title', u'user'])

            if u'photos' in tables:
                photos_data = sqlite_processor.read_sqlite_table(
                    file_path, u'photos', [u'_id', u'album_id', u'cache_pathname', u'content_type', u'content_url',
                                           u'date_edited', u'date_published', u'date_taken', u'date_updated',
                                           u'html_page_url', u'latitude', u'longitude', u'size', u'sync_account',
                                           u'title'])

            if u'users' in tables:
                users_data = sqlite_processor.read_sqlite_table(
                    file_path, u'users', ['_id', 'account'])

    return file_info_data, download_data, albums_data, photos_data, users_data