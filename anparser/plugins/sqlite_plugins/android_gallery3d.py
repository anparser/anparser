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
    file_database = None
    download_database = None
    picasa_database = None
    file_info_data = None
    download_data = None
    albums_data = None
    photos_data = None
    users_data = None

    for file_path in file_list:
        if file_path.endswith('FileInfo.db'):
            file_database = file_path
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
            download_database = file_path
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
            picasa_database = file_path
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
            gallery_data['Database'] = file_database
            gallery_data['Table'] = 'file_info'
            gallery_data['Download Id'] = ''
            gallery_data['File Path'] = entry['file_path']
            gallery_data['Data'] = ''
            gallery_data['Content Url'] = ''
            gallery_data['Hash Key'] = entry['hash_key']
            gallery_data['Hash Code'] = ''
            gallery_data['File Info Type'] = entry['file_info_type']
            gallery_data['Last Access'] = ''
            gallery_data['Last Updated'] = ''
            gallery_data['Size'] = ''

            file_data_list.append(gallery_data)
            gallery_data = OrderedDict()

    # Add data from download.db to file_data_list
    # Add data from download table to gallery_data
    if download_data:
        for entry in download_data:
            gallery_data['Database'] = download_database
            gallery_data['Table'] = 'download'
            gallery_data['Download Id'] = entry['_id']
            gallery_data['File Path'] = ''
            gallery_data['Data'] = entry['_data']
            gallery_data['Content Url'] = entry['content_url']
            gallery_data['Hash Key'] = ''
            gallery_data['Hash Code'] = entry['hash_code']
            gallery_data['File Info Type'] = ''
            try:
                gallery_data['Last Access'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['last_access'] / 1000.))
            except TypeError:
                gallery_data['Last Access'] = ''
            try:
                gallery_data['Last Updated'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['last_updated'] / 1000.))
            except TypeError:
                gallery_data['Last Updated'] = ''
            gallery_data['Size'] = entry['_size']

            file_data_list.append(gallery_data)
            gallery_data = OrderedDict()

    # Add data from picasa.db to picasa_data_list
    # Add data from users table to gallery_data
    if users_data:
        for entry in users_data:
            gallery_data['Database'] = picasa_database
            gallery_data['Table'] = 'users'
            gallery_data['User Id'] = entry['_id']
            gallery_data['Photo Id'] = ''
            gallery_data['Album Id'] = ''
            gallery_data['Account'] = entry['account']
            gallery_data['User'] = ''
            gallery_data['Title'] = ''
            gallery_data['Summary'] = ''
            gallery_data['# Photos'] = ''
            gallery_data['Size'] = ''
            gallery_data['Content Type'] = ''
            gallery_data['Date Taken'] = ''
            gallery_data['Date Edited'] = ''
            gallery_data['Date Updated'] = ''
            gallery_data['Date Published'] = ''
            gallery_data['Location'] = ''
            gallery_data['Latitude'] = ''
            gallery_data['Longitude'] = ''
            gallery_data['Cache Path Name'] = ''
            gallery_data['Content Url'] = ''
            gallery_data['Html Page Url'] = ''

            picasa_data_list.append(gallery_data)
            gallery_data = OrderedDict()

    # Add data from albums table to gallery_data
    if albums_data:
        for entry in albums_data:
            gallery_data['Database'] = picasa_database
            gallery_data['Table'] = 'albums'
            gallery_data['User Id'] = ''
            gallery_data['Photo Id'] = ''
            gallery_data['Album Id'] = entry['_id']
            gallery_data['Account'] = entry['sync_account']
            gallery_data['User'] = entry['user']
            gallery_data['Title'] = entry['title']
            gallery_data['Summary'] = entry['summary']
            gallery_data['# Photos'] = entry['num_photos']
            gallery_data['Size'] = entry['bytes_used']
            gallery_data['Content Type'] = ''
            gallery_data['Date Taken'] = ''
            try:
                gallery_data['Date Edited'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['date_edited'] / 1000.))
            except TypeError:
                gallery_data['Date Edited'] = ''
            try:
                gallery_data['Date Published'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['date_published'] / 1000.))
            except TypeError:
                gallery_data['Date Published'] = ''
            try:
                gallery_data['Date Updated'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['date_updated'] / 1000.))
            except TypeError:
                gallery_data['Date Updated'] = ''
            gallery_data['Location'] = entry['location_string']
            gallery_data['Latitude'] = ''
            gallery_data['Longitude'] = ''
            gallery_data['Cache Path Name'] = ''
            gallery_data['Content Url'] = ''
            gallery_data['Html Page Url'] = entry['html_page_url']

            picasa_data_list.append(gallery_data)
            gallery_data = OrderedDict()

    # Add data from photos table to gallery_data
    if photos_data:
        for entry in photos_data:
            gallery_data['Database'] = picasa_database
            gallery_data['Table'] = 'photos'
            gallery_data['User Id'] = ''
            gallery_data['Photo Id'] = entry['_id']
            gallery_data['Album Id'] = entry['album_id']
            gallery_data['Account'] = entry['sync_account']
            gallery_data['User'] = ''
            gallery_data['Title'] = entry['title']
            gallery_data['Summary'] = ''
            gallery_data['# Photos'] = ''
            gallery_data['Size'] = entry['size']
            gallery_data['Content Type'] = entry['content_type']
            try:
                gallery_data['Date Taken'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['date_taken'] / 1000.))
            except TypeError:
                gallery_data['Date Taken'] = ''
            try:
                gallery_data['Date Edited'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['date_edited'] / 1000.))
            except TypeError:
                gallery_data['Date Edited'] = ''
            try:
                gallery_data['Date Published'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['date_published'] / 1000.))
            except TypeError:
                gallery_data['Date Published'] = ''
            try:
                gallery_data['Date Updated'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(
                    entry['date_updated'] / 1000.))
            except TypeError:
                gallery_data['Date Updated'] = ''
            gallery_data['Location'] = ''
            gallery_data['Latitude'] = entry['latitude']
            gallery_data['Longitude'] = entry['longitude']
            gallery_data['Cache Path Name'] = entry['cache_pathname']
            gallery_data['Content Url'] = entry['content_url']
            gallery_data['Html Page Url'] = entry['html_page_url']

            picasa_data_list.append(gallery_data)
            gallery_data = OrderedDict()


    return file_data_list, picasa_data_list