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

from processors import sqlite_processor, time_processor


def teslacoilsw_launcher(file_list):
    """
    Parses launcher.db database from com.teslacoilsw.launcher

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: allapps, favorites
    allapps_data = None
    favorites_data = None

    for file_path in file_list:
        if file_path.endswith(u'launcher.db') and file_path.count(u'com.teslacoilsw.launcher') > 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)

            if u'allapps' in tables:
                allapps_data = sqlite_processor.read_sqlite_table(
                    file_path, u'allapps',
                    u'componentName, title, lastUpdateTime')
                if allapps_data is not None:
                    allapps_data.lastUpdateTime = time_processor.unix_time(allapps_data.lastUpdateTime)

            if u'favorites' in tables:
                favorites_data = sqlite_processor.read_sqlite_table(
                    file_path, u'favorites',
                    u'_id, title, intent')

    return allapps_data, favorites_data