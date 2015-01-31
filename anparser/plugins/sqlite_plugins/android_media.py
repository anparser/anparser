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

import logging
import sqlite_processor


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
        if file_path.endswith(u'external.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'files' in tables:
                external_data = sqlite_processor.read_sqlite_table(
                    file_path, u'files', [u'_id', u'_data', u'_size', u'date_added', u'date_modified', u'mime_type',
                                          u'title', u'description', u'_display_name', u'latitude', u'longitude',
                                          u'datetaken', u'is_ringtone', u'is_music', u'is_alarm', u'is_notification',
                                          u'is_podcast', u'date_played', u'count_played', u'width', u'height',
                                          u'video_filetype', u'video_iswatched'])

        if file_path.endswith(u'internal.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'files' in tables:
                internal_data = sqlite_processor.read_sqlite_table(
                    file_path, u'files', [u'_id', u'_data', u'_size', u'date_added', u'date_modified', u'mime_type',
                                          u'title', u'description', u'_display_name', u'latitude', u'longitude',
                                          u'datetaken', u'is_ringtone', u'is_music', u'is_alarm', u'is_notification',
                                          u'is_podcast', u'date_played', u'count_played', u'width', u'height',
                                          u'video_filetype', u'video_iswatched'])

    return external_data, internal_data