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
__date__ = '20150125'
__version__ = '0.00'

from ingest import sqlite_processor  # , time_processor


def samsung_galaxyfinder(file_list):
    """
    Parses Tag.db database from com.samsung.android.app.galaxyfinder

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: contents, tagging, tags
    contents_data = None
    tagging_data = None
    tags_data = None

    for file_path in file_list:
        if file_path.endswith(u'Tag.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'contents' in tables:
                contents_data = sqlite_processor.read_sqlite_table(
                    file_path, u'contents',
                    u'_id, timestamp, contenturi, appname, filepath')
                if contents_data is not None:
                    contents_data.timestamp = time_processor.unix_time(contents_data.timestamp)

            if u'tagging' in tables:
                tagging_data = sqlite_processor.read_sqlite_table(
                    file_path, u'tagging',
                    u'_id, content_id, tag_id')

            if u'tags' in tables:
                tags_data = sqlite_processor.read_sqlite_table(
                    file_path, u'tags',
                    u'_id, type, rawdata, data')

    return contents_data, tagging_data, tags_data