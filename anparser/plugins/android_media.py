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


def android_media(file_list):
    """
    Parses external and internal databases from com.android.providers.media

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # Initialize table variables: external_files and internal_files
    external_data = None
    internal_data = None

    for file_path in file_list:
        if file_path.endswith('external.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'files' in tables:
                try:
                    external_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'files',
                        columns='_id, _data, _size, date_added, date_modified, '
                                'mime_type, title, description, _display_name, '
                                'latitude, longitude, datetaken, is_ringtone,'
                                'is_music, is_alarm, is_notification, is_podcast, '
                                'date_played, count_played, width, height, '
                                'video_filetype, video_iswatched')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('internal.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'files' in tables:
                try:
                    internal_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'files',
                        columns='_id, _data, _size, date_added, date_modified, '
                                'mime_type, title, description, _display_name, '
                                'latitude, longitude, datetaken, is_ringtone,'
                                'is_music, is_alarm, is_notification, is_podcast, '
                                'date_played, count_played, width, height, '
                                'video_filetype, video_iswatched')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    media_data_list = []
    media_data = OrderedDict()

    # Add data from external.db to media_data_list
    # Add data from files table to media_data
    if external_data:
        for entry in external_data:
            media_data['Table'] = 'external - files'
            media_data['id'] = entry[0]
            media_data['data'] = entry[1]
            media_data['size'] = entry[2]
            try:
                media_data['created'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3]))
            except (TypeError, ValueError):
                media_data['created'] = ''
            try:
                media_data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4]))
            except (TypeError, ValueError):
                media_data['modified'] = ''
            media_data['mime type'] = entry[5]
            media_data['title'] = entry[6]
            media_data['description'] = entry[7]
            media_data['display name'] = entry[8]
            media_data['latitude'] = entry[9]
            media_data['longitude'] = entry[10]
            try:
                media_data['date taken'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[11]))
            except (TypeError, ValueError):
                media_data['date taken'] = ''
            media_data['is ringtone'] = entry[12]
            media_data['is music'] = entry[13]
            media_data['is alarm'] = entry[14]
            media_data['is notification'] = entry[15]
            media_data['is podcast'] = entry[16]
            try:
                media_data['date played'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[17]))
            except (TypeError, ValueError):
                media_data['date played'] = ''
            media_data['count played'] = entry[18]
            media_data['width'] = entry[19]
            media_data['height'] = entry[20]
            media_data['video filetype'] = entry[21]
            media_data['video is watched'] = entry[22]

            media_data_list.append(media_data)
            media_data = OrderedDict()

    # Add data from internal.db to media_data_list
    # Add data from files table to media_data
    if internal_data:
        for entry in internal_data:
            media_data['Table'] = 'internal - files'
            media_data['id'] = entry[0]
            media_data['data'] = entry[1]
            media_data['size'] = entry[2]
            try:
                media_data['created'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3]))
            except (TypeError, ValueError):
                media_data['created'] = ''
            try:
                media_data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4]))
            except (TypeError, ValueError):
                media_data['modified'] = ''
            media_data['mime type'] = entry[5]
            media_data['title'] = entry[6]
            media_data['description'] = entry[7]
            media_data['display name'] = entry[8]
            media_data['latitude'] = entry[9]
            media_data['longitude'] = entry[10]
            try:
                media_data['date taken'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[11]))
            except (TypeError, ValueError):
                media_data['date taken'] = ''
            media_data['is ringtone'] = entry[12]
            media_data['is music'] = entry[13]
            media_data['is alarm'] = entry[14]
            media_data['is notification'] = entry[15]
            media_data['is podcast'] = entry[16]
            try:
                media_data['date played'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[17]))
            except (TypeError, ValueError):
                media_data['date played'] = ''
            media_data['count played'] = entry[18]
            media_data['width'] = entry[19]
            media_data['height'] = entry[20]
            media_data['video filetype'] = entry[21]
            media_data['video is watched'] = entry[22]

            media_data_list.append(media_data)
            media_data = OrderedDict()

    return media_data_list