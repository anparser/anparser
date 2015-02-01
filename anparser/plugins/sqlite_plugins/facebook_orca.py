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
__date__ = '20150108'
__version__ = '0.00'

from ingest import sqlite_processor  # , time_processor


def facebook_orca(file_list):
    """
    Parses database folder from com.facebook.orca "Facebook Messenger"

    :param file_list: List of all files
    :return: Dictionary of parsed data from databases
    """
    # TODO: Add support for group_conversations table in threads_db2.
    # Initialize table variables: contacts, folder_counts, folders, messages, thread_users, threads
    contacts_database = None
    threads_database = None
    contacts_data = None
    folder_counts_data = None
    folders_data = None
    messages_data = None
    thread_users_data = None
    threads_data = None

    for file_path in file_list:
        if file_path.endswith(u'contacts_db2') and file_path.count(u'com.facebook.orca') > 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'contacts' in tables:
                contacts_data = sqlite_processor.read_sqlite_table(
                    file_path, u'contacts',
                    u'internal_id, contact_id, fbid, first_name, last_name, display_name')

        if file_path.endswith(u'threads_db2') and file_path.count(u'com.facebook.orca') > 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'folder_counts' in tables:
                folder_counts_data = sqlite_processor.read_sqlite_table(
                    file_path, u'folder_counts',
                    u'folder, unread_count, unseen_count, last_seen_time, last_action_id')
                if folder_counts_data is not None:
                    folder_counts_data.last_seen_time = time_processor.unix_time(folder_counts_data.last_seen_time)

            if u'folders' in tables:
                folders_data = sqlite_processor.read_sqlite_table(
                    file_path, u'folders',
                    u'folder, thread_key, timestamp_ms')
                if folders_data is not None:
                    folders_data.timestamp_ms = time_processor.unix_time(folders_data.timestamp_ms)

            if u'messages' in tables:
                messages_data = sqlite_processor.read_sqlite_table(
                    file_path, u'messages',
                    u'msg_id, thread_key, action_id, text, sender, timestamp_ms, '
                    u'timestamp_sent_ms, attachments, coordinates, offline_threading_id, '
                    u'source, send_error, send_error_message')
                if messages_data is not None:
                    messages_data.timestamp_ms = time_processor.unix_time(messages_data.timestamp_ms)
                    messages_data.timestamp_sent_ms = time_processor.unix_time(messages_data.timestamp_sent_ms)

            if u'thread_users' in tables:
                thread_users_data = sqlite_processor.read_sqlite_table(
                    file_path, u'thread_users',
                    u'user_key, first_name, last_name, name')

            if u'threads' in tables:
                threads_data = sqlite_processor.read_sqlite_table(
                    file_path, u'threads',
                    u'thread_key, thread_fbid, action_id, name, '
                    u'participants, former_participants, senders, '
                    u'timestamp_ms, last_fetch_time_ms, unread, '
                    u'folder')
                if threads_data is not None:
                    threads_data.timestamp_ms = time_processor.unix_time(threads_data.timestamp_ms)
                    threads_data.last_fetch_time_ms = time_processor.unix_time(threads_data.last_fetch_time_ms)

    return contacts_data, folder_counts_data, folders_data, messages_data, thread_users_data, threads_data