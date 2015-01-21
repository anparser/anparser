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
import __init__
import time


def android_gallery3d(file_list):
    """
    Parses databases from com.android.gallery3d

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # Initialize table variables: file_info, download, albums, photos, users
    file_info_data = None
    download_data = None
    albums_data = None
    photos_data = None
    users_data = None

    for file_path in file_list:
        if file_path.endswith('FileInfo.db'):
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'file_info' in tables:
                try:
                    file_info_data = __init__.read_sqlite_table(
                        file_path, 'file_info',
                        columns='hash_key, file_path, file_info_type')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('download.db') and file_path.count('gallery3d') > 0:
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'download' in tables:
                try:
                    download_data = __init__.read_sqlite_table(
                        file_path, 'download',
                        columns='_id, _data, content_url, hash_code, last_access, '
                                'last_updated, _size')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('picasa.db'):
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'albums' in tables:
                try:
                    albums_data = __init__.read_sqlite_table(
                        file_path, 'albums',
                        columns='_id, bytes_used, date_edited, date_published, date_updated, '
                                'html_page_url, location_string, num_photos, '
                                'summary, sync_account, title, user')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'photos' in tables:
                try:
                    photos_data = __init__.read_sqlite_table(
                        file_path, 'photos',
                        columns='_id, album_id, cache_pathname, content_type, content_url, '
                                'date_edited, date_published, date_taken, date_updated, '
                                'html_page_url, latitude, longitude, size, sync_account, '
                                'title')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'users' in tables:
                try:
                    users_data = __init__.read_sqlite_table(
                        file_path, 'users',
                        columns='_id, account')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass


    file_data_list = []
    picasa_data_list = []
    gallery_data = OrderedDict()

    # Add data from FileInfo.db to file_data_list
    # Add data from file_info table to gallery_data
    if file_info_data:
        for entry in file_info_data:
            gallery_data['Table'] = 'file_info'
            gallery_data['download id'] = ''
            gallery_data['file path'] = entry[1]
            gallery_data['data'] = ''
            gallery_data['content url'] = ''
            gallery_data['hash key'] = entry[0]
            gallery_data['hash code'] = ''
            gallery_data['file info type'] = entry[2]
            gallery_data['last access'] = ''
            gallery_data['last updated'] = ''
            gallery_data['size'] = ''

            file_data_list.append(gallery_data)
            gallery_data = OrderedDict()

    # Add data from download.db to file_data_list
    # Add data from download table to gallery_data
    if download_data:
        for entry in download_data:
            gallery_data['Table'] = 'download'
            gallery_data['download id'] = entry[0]
            gallery_data['file path'] = ''
            gallery_data['data'] = entry[1]
            gallery_data['content url'] = entry[2]
            gallery_data['hash key'] = ''
            gallery_data['hash code'] = entry[3]
            gallery_data['file info type'] = ''
            try:
                gallery_data['last access'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.))
            except TypeError:
                gallery_data['last access'] = ''
            try:
                gallery_data['last updated'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                gallery_data['last updated'] = ''
            gallery_data['size'] = entry[6]

            file_data_list.append(gallery_data)
            gallery_data = OrderedDict()

    # Add data from picasa.db to picasa_data_list
    # Add data from users table to gallery_data
    if users_data:
        for entry in users_data:
            gallery_data['Table'] = 'users'
            gallery_data['user id'] = entry[0]
            gallery_data['photo id'] = ''
            gallery_data['album id'] = ''
            gallery_data['account'] = entry[1]
            gallery_data['user'] = ''
            gallery_data['title'] = ''
            gallery_data['summary'] = ''
            gallery_data['num photos'] = ''
            gallery_data['size'] = ''
            gallery_data['content type'] = ''
            gallery_data['date taken'] = ''
            gallery_data['date edited'] = ''
            gallery_data['date updated'] = ''
            gallery_data['date published'] = ''
            gallery_data['location'] = ''
            gallery_data['latitude'] = ''
            gallery_data['longitude'] = ''
            gallery_data['cache pathname'] = ''
            gallery_data['content url'] = ''
            gallery_data['html page url'] = ''

            picasa_data_list.append(gallery_data)
            gallery_data = OrderedDict()

    # Add data from albums table to gallery_data
    if albums_data:
        for entry in albums_data:
            gallery_data['Table'] = 'albums'
            gallery_data['user id'] = ''
            gallery_data['photo id'] = ''
            gallery_data['album id'] = entry[0]
            gallery_data['account'] = entry[9]
            gallery_data['user'] = entry[11]
            gallery_data['title'] = entry[10]
            gallery_data['summary'] = entry[8]
            gallery_data['num photos'] = entry[7]
            gallery_data['size'] = entry[1]
            gallery_data['content type'] = ''
            gallery_data['date taken'] = ''
            try:
                gallery_data['date edited'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.))
            except TypeError:
                gallery_data['date edited'] = ''
            try:
                gallery_data['date published'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                gallery_data['date published'] = ''
            try:
                gallery_data['date updated'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.))
            except TypeError:
                gallery_data['date updated'] = ''
            gallery_data['location'] = entry[6]
            gallery_data['latitude'] = ''
            gallery_data['longitude'] = ''
            gallery_data['cache pathname'] = ''
            gallery_data['content url'] = ''
            gallery_data['html page url'] = entry[5]

            picasa_data_list.append(gallery_data)
            gallery_data = OrderedDict()

    # Add data from photos table to gallery_data
    if photos_data:
        for entry in photos_data:
            gallery_data['Table'] = 'photos'
            gallery_data['user id'] = ''
            gallery_data['photo id'] = entry[0]
            gallery_data['album id'] = entry[1]
            gallery_data['account'] = entry[13]
            gallery_data['user'] = ''
            gallery_data['title'] = entry[14]
            gallery_data['summary'] = ''
            gallery_data['num photos'] = ''
            gallery_data['size'] = entry[12]
            gallery_data['content type'] = entry[3]
            try:
                gallery_data['date taken'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[7] / 1000.))
            except TypeError:
                gallery_data['date taken'] = ''
            try:
                gallery_data['date edited'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                gallery_data['date edited'] = ''
            try:
                gallery_data['date published'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[6] / 1000.))
            except TypeError:
                gallery_data['date published'] = ''
            try:
                gallery_data['date updated'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[8] / 1000.))
            except TypeError:
                gallery_data['date updated'] = ''
            gallery_data['location'] = ''
            gallery_data['latitude'] = entry[10]
            gallery_data['longitude'] = entry[11]
            gallery_data['cache pathname'] = entry[2]
            gallery_data['content url'] = entry[4]
            gallery_data['html page url'] = entry[9]

            picasa_data_list.append(gallery_data)
            gallery_data = OrderedDict()


    return file_data_list, picasa_data_list