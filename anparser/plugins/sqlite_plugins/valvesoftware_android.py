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
__date__ = '20150124'
__version__ = '0.00'

import logging
import sqlite_processor


def valvesoftware_android(file_list):
    """
    Parses databases from com.valvesoftware.android.steam.community

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: debug, message
    debug_data = None
    message_data = None
    friends_data = None

    for file_path in file_list:
        if file_path.endswith(u'dbgutil.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'dbgutil' in tables:
                debug_data = sqlite_processor.read_sqlite_table(
                    file_path, u'dbgutil',
                    u'_id, msgtime, key, value')

        if file_path.endswith(u'umqcomm.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)

            if u'UmqInfo' in tables:
                friends_data = sqlite_processor.read_sqlite_table(
                    file_path, u'UmqInfo',
                    u'id1, id2, name')

            if u'UmqMsg' in tables:
                message_data = sqlite_processor.read_sqlite_table(
                    file_path, u'UmqMsg',
                    u'_id, myuser1, myuser2, wuser1, wuser2, msgincoming, msgunread, '
                    u'msgtime, msgtype, bindata')

    return debug_data, friends_data, message_data