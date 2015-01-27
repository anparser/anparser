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


def android_media(file_list):
    """
    Parses external and internal databases from com.android.providers.media

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # Initialize table variables: external_files and internal_files
    external_database = None
    internal_database = None
    external_data = None
    internal_data = None

    for file_path in file_list:
        if file_path.endswith('external.db'):
            external_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'files' in tables:
                try:
                    external_data = __init__.read_sqlite_table(
                        file_path, 'files',
                        columns='_id, _data, _size, date_added, date_modified, '
                                'mime_type, title, description, _display_name, '
                                'latitude, longitude, datetaken, is_ringtone,'
                                'is_music, is_alarm, is_notification, is_podcast, '
                                'date_played, count_played, width, height, '
                                'video_filetype, video_iswatched')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('internal.db'):
            internal_data = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'files' in tables:
                try:
                    internal_data = __init__.read_sqlite_table(
                        file_path, 'files',
                        columns='_id, _data, _size, date_added, date_modified, '
                                'mime_type, title, description, _display_name, '
                                'latitude, longitude, datetaken, is_ringtone,'
                                'is_music, is_alarm, is_notification, is_podcast, '
                                'date_played, count_played, width, height, '
                                'video_filetype, video_iswatched')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    media_data_list = []
    media_data = OrderedDict()

    # Add data from external.db to media_data_list
    # Add data from files table to media_data
    if external_data:
        for entry in external_data:
            media_data['Database'] = external_database
            media_data['Table'] = 'files'
            media_data['Id'] = entry['_id']
            media_data['Data'] = entry['_data']
            media_data['Size'] = entry['_size']
            try:
                media_data['Created'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['date_added']))
            except (TypeError, ValueError):
                media_data['Created'] = ''
            try:
                media_data['Modified'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['date_modified']))
            except (TypeError, ValueError):
                media_data['Modified'] = ''
            media_data['Mime Type'] = entry['mime_type']
            media_data['Title'] = entry['title']
            media_data['Description'] = entry['description']
            media_data['Display Name'] = entry['_display_name']
            media_data['Latitude'] = entry['latitude']
            media_data['Longitude'] = entry['longitude']
            try:
                media_data['Date Taken'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['datetaken']))
            except (TypeError, ValueError):
                media_data['Date Taken'] = ''
            media_data['Is Ringtone'] = entry['is_ringtone']
            media_data['Is Music'] = entry['is_music']
            media_data['Is Alarm'] = entry['is_alarm']
            media_data['Is Notification'] = entry['is_notification']
            media_data['Is Podcast'] = entry['is_podcast']
            try:
                media_data['Date Played'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['date_played']))
            except (TypeError, ValueError):
                media_data['Date Played'] = ''
            media_data['Count Played'] = entry['count_played']
            media_data['Width'] = entry['width']
            media_data['Height'] = entry['height']
            media_data['Video File Type'] = entry['video_filetype']
            media_data['Video Is Watched'] = entry['video_iswatched']

            media_data_list.append(media_data)
            media_data = OrderedDict()

    # Add data from internal.db to media_data_list
    # Add data from files table to media_data
    if internal_data:
        for entry in internal_data:
            media_data['Database'] = internal_database
            media_data['Table'] = 'files'
            media_data['Id'] = entry['_id']
            media_data['Data'] = entry['_data']
            media_data['Size'] = entry['_size']
            try:
                media_data['Created'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['date_added']))
            except (TypeError, ValueError):
                media_data['Created'] = ''
            try:
                media_data['Modified'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['date_modified']))
            except (TypeError, ValueError):
                media_data['Modified'] = ''
            media_data['Mime Type'] = entry['mime_type']
            media_data['Title'] = entry['title']
            media_data['Description'] = entry['description']
            media_data['Display Name'] = entry['_display_name']
            media_data['Latitude'] = entry['latitude']
            media_data['Longitude'] = entry['longitude']
            try:
                media_data['Date Taken'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['datetaken']))
            except (TypeError, ValueError):
                media_data['Date Taken'] = ''
            media_data['Is Ringtone'] = entry['is_ringtone']
            media_data['Is Music'] = entry['is_music']
            media_data['Is Alarm'] = entry['is_alarm']
            media_data['Is Notification'] = entry['is_notification']
            media_data['Is Podcast'] = entry['is_podcast']
            try:
                media_data['Date Played'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry['date_played']))
            except (TypeError, ValueError):
                media_data['Date Played'] = ''
            media_data['Count Played'] = entry['count_played']
            media_data['Width'] = entry['width']
            media_data['Height'] = entry['height']
            media_data['Video File Type'] = entry['video_filetype']
            media_data['Video Is Watched'] = entry['video_iswatched']

            media_data_list.append(media_data)
            media_data = OrderedDict()

    return media_data_list