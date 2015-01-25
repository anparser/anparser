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

from collections import OrderedDict
import logging
import __init__
import time


def samsung_galaxyfinder(file_list):
    """
    Parses Tag.db database from com.samsung.android.app.galaxyfinder

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: contents, tagging, tags
    tag_database = None
    contents_data = None
    tagging_data = None
    tags_data = None

    for file_path in file_list:
        if file_path.endswith('Tag.db'):
            tag_database = file_path
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'contents' in tables:
                try:
                    contents_data = __init__.read_sqlite_table(
                        file_path, 'contents',
                        columns='_id, timestamp, contenturi, appname, filepath')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'tagging' in tables:
                try:
                    tagging_data = __init__.read_sqlite_table(
                        file_path, 'tagging',
                        columns='_id, content_id, tag_id')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'tags' in tables:
                try:
                    tags_data = __init__.read_sqlite_table(
                        file_path, 'tags',
                        columns='_id, type, rawdata, data')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    galaxyfinder_tags_list = []
    galaxyfinder_data = OrderedDict()

    # Add tables from Tag.db to galaxyfinder_tags_list
    # Add data from tagging table to galaxyfinder_data
    if tagging_data:
        for entry in tagging_data:
            galaxyfinder_data['Database'] = tag_database
            galaxyfinder_data['Table'] = 'tagging'
            galaxyfinder_data['Tagging Id'] = entry[0]
            galaxyfinder_data['Tag Id'] = entry[2]
            galaxyfinder_data['Content Id'] = entry[1]
            galaxyfinder_data['Tag Type'] = ''
            galaxyfinder_data['Tag Rawdata'] = ''
            galaxyfinder_data['Tag Data'] = ''
            galaxyfinder_data['Content Uri'] = ''
            galaxyfinder_data['App Name'] = ''
            galaxyfinder_data['File Path'] = ''
            galaxyfinder_data['Timestamp'] = ''


            galaxyfinder_tags_list.append(galaxyfinder_data)
            galaxyfinder_data = OrderedDict()

    # Add data from tags table to galaxyfinder_data
    if tags_data:
        for entry in tags_data:
            galaxyfinder_data['Database'] = tag_database
            galaxyfinder_data['Table'] = 'tags'
            galaxyfinder_data['Tagging Id'] = ''
            galaxyfinder_data['Tag Id'] = entry[0]
            galaxyfinder_data['Content Id'] = ''
            galaxyfinder_data['Tag Type'] = entry[1]
            galaxyfinder_data['Tag Rawdata'] = entry[2]
            galaxyfinder_data['Tag Data'] = entry[3]
            galaxyfinder_data['Content Uri'] = ''
            galaxyfinder_data['App Name'] = ''
            galaxyfinder_data['File Path'] = ''
            galaxyfinder_data['Timestamp'] = ''

            galaxyfinder_tags_list.append(galaxyfinder_data)
            galaxyfinder_data = OrderedDict()

    # Add data from contents table to galaxyfinder_data
    if contents_data:
        for entry in contents_data:
            galaxyfinder_data['Database'] = tag_database
            galaxyfinder_data['Table'] = 'contents'
            galaxyfinder_data['Tagging Id'] = ''
            galaxyfinder_data['Tag Id'] = ''
            galaxyfinder_data['Content Id'] = entry[0]
            galaxyfinder_data['Tag Type'] = ''
            galaxyfinder_data['Tag Rawdata'] = ''
            galaxyfinder_data['Tag Data'] = ''
            galaxyfinder_data['Content Uri'] = entry[2]
            galaxyfinder_data['App Name'] = entry[3]
            galaxyfinder_data['File Path'] = entry[4]
            try:
                galaxyfinder_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[1] / 1000.))
            except TypeError:
                galaxyfinder_data['Timestamp'] = ''

            galaxyfinder_tags_list.append(galaxyfinder_data)
            galaxyfinder_data = OrderedDict()

    return galaxyfinder_tags_list