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
__date__ = '20150215'
__version__ = '0.00'

from ingest import sqlite_processor, time_processor


def sh_whisper(file_list):
    """
    Parses databases from sh.whisper

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: contents, tagging, tags
    conversations_data = None
    messages_data = None
    whisper_data = None
    groups_data = None
    notification_data = None

    for file_path in file_list:
        if file_path.endswith(u'c.db') and file_path.count('sh.whisper') > 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'c' in tables:
                conversations_data = sqlite_processor.read_sqlite_table(
                    file_path, u'c',
                    u'_id, cid, pid, sid, gt, lm, unread, fav, inbox_hide, ts, blocked')
                if conversations_data is not None:
                    conversations_data.ts = time_processor.unix_time(conversations_data.ts)
                    conversations_data['Database Path'] = file_path

            if u'm' in tables:
                messages_data = sqlite_processor.read_sqlite_table(
                    file_path, u'm',
                    u'_id, c_id, mid, ts, sid, text, gt, mine, unread, sent, hasimage, del')
                if messages_data is not None:
                    messages_data.ts = time_processor.unix_time(messages_data.ts)
                    messages_data['Database Path'] = file_path

        if file_path.endswith(u'w.db') and file_path.count('sh.whisper') > 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'w' in tables:
                whisper_data = sqlite_processor.read_sqlite_table(
                    file_path, u'w',
                    u'_id, puid, user, ts, location, parent, text, hearts, replies, lat, lon, groups')
                if whisper_data is not None:
                    whisper_data.ts = time_processor.unix_time(whisper_data.ts)
                    whisper_data['Database Path'] = file_path

            if u'groups' in tables:
                groups_data = sqlite_processor.read_sqlite_table(
                    file_path, u'groups',
                    u'_id, uid, name, short_name, type')
                if groups_data is not None:
                    groups_data['Database Path'] = file_path

            if u'n' in tables:
                notification_data = sqlite_processor.read_sqlite_table(
                    file_path, u'n',
                    u'_id, type, wid, message, ts, read')
                if notification_data is not None:
                    notification_data.ts = time_processor.unix_time(notification_data.ts)
                    notification_data['Database Path'] = file_path

    return conversations_data, messages_data, whisper_data, groups_data, notification_data
