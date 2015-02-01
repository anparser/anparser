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
__date__ = '20150119'
__version__ = '0.00'

from ingest import sqlite_processor  # , time_processor


def kik_android(file_list):
    """
    Parses kikDatabase.db database from kik.android

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: KIKContentTable, KIKcontactsTable, messagesTable
    content_data = None
    contacts_data = None
    messages_data = None

    for file_path in file_list:
        if file_path.endswith(u'kikDatabase.db'):
            kik_database = file_path
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'KIKContentTable' in tables:
                content_data = sqlite_processor.read_sqlite_table(
                    file_path, u'KIKContentTable',
                    u'_id, content_id, content_type, content_name, content_string')

            if u'KIKcontactsTable' in tables:
                contacts_data = sqlite_processor.read_sqlite_table(
                    file_path, u'KIKcontactsTable',
                    u'_id, jid, display_name, user_name, is_blocked, is_ignored')

            if u'messagesTable' in tables:
                messages_data = sqlite_processor.read_sqlite_table(
                    file_path, u'messagesTable',
                    u'_id, body, partner_jid, was_me, read_state, uid, length, timestamp, content_id, app_id')
                if messages_data is not None:
                    messages_data.timestamp = time_processor.unix_time(messages_data.timestamp)

    return content_data, contacts_data, messages_data