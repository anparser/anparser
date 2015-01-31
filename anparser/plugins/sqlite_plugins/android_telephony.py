# -*- coding: utf-8 -*-
"""
anparser - an Open Source Android Artifact Parser
Copyright (C) 2015  Chapin Bryce

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

__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '20150102'
__version__ = '0.00'

import logging
import sqlite_processor

def android_telephony(file_listing):
    """

    :param file_listing:
    :return:
    """

    sms_data = None
    threads_data = None


    for file_path in file_listing:
        if file_path.endswith(u'mmssms.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'sms' in tables:
                sms_data = sqlite_processor.read_sqlite_table(
                    file_path, u'sms', u'_id, thread_id, address, person, date, date_sent, body, read, seen')

            if u'threads' in tables:
                threads_data = sqlite_processor.read_sqlite_table(
                    file_path, u'threads', u'_id, date, message_count, snippet, read, has_attachment')

    return sms_data, threads_data