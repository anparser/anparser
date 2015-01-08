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

from collections import OrderedDict
import logging
import sqlite_plugins
import time


def facebook_orca(file_list):
    """
    Parses database folder from com.facebook.orca "Facebook Messenger"

    :param file_list: List of all files
    :return: Dictionary of parsed data from databases
    """
    # TODO: Add support for group_conversations table in threads_db2.
    # Initialize table variables: contacts, folder_counts, folders, messages, thread_users, threads
    contacts_data = None
    folder_counts_data = None
    folders_data = None
    messages_data = None
    thread_users_data = None
    threads_data = None

    for file_path in file_list:
        if file_path.endswith('contacts_db2') and file_path.count('com.facebook.orca') > 0:
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'contacts' in tables:
                try:
                    contacts_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'contacts',
                        columns='internal_id, contact_id, fbid, first_name, last_name, '
                                'display_name')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('threads_db2') and file_path.count('com.facebook.orca') > 0:
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'folder_counts' in tables:
                try:
                    folder_counts_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'folder_counts',
                        columns='folder, unread_count, unseen_count, last_seen_time, last_action_id')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'folders' in tables:
                try:
                    folders_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'folders',
                        columns='folder, thread_key, timestamp_ms')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'messages' in tables:
                try:
                    messages_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'messages',
                        columns='msg_id, thread_key, action_id, text, sender, timestamp_ms, '
                                'timestamp_sent_ms, attachments, coordinates, offline_threading_id, '
                                'source, send_error, send_error_message')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'thread_users' in tables:
                thread_users_data = sqlite_plugins.read_sqlite_table(
                    file_path, 'thread_users',
                    columns='user_key, first_name, last_name, name')
            if 'threads' in tables:
                try:
                    threads_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'threads',
                        columns='thread_key, thread_fbid, action_id, name, '
                                'participants, former_participants, senders, '
                                'timestamp_ms, last_fetch_time_ms, unread, '
                                'folder')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    orca_contacts_list = []
    orca_msg_list = []
    orca_threads_list = []
    orca_data = OrderedDict()

    # Add data from contacts_db2 database to orca_contacts_list
    # Add data from contacts table to orca_data
    if contacts_data:
        for entry in contacts_data:
            orca_data['Table'] = 'contacts'
            orca_data['id'] = entry[0]
            orca_data['contact id'] = entry[1]
            orca_data['FaceBook id'] = entry[2]
            orca_data['first name'] = entry[3]
            orca_data['last name'] = entry[4]
            orca_data['name'] = entry[5]

            orca_contacts_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from threads_db2 database to orca_threads_list
    # Add data from folder_counts table to orca_data
    if folder_counts_data:
        for entry in folder_counts_data:
            orca_data['Table'] = 'folder_counts'
            orca_data['folder'] = entry[0]
            orca_data['thread'] = ''
            orca_data['thread id'] = ''
            orca_data['FaceBook id'] = ''
            orca_data['first name'] = ''
            orca_data['last name'] = ''
            orca_data['name'] = ''
            orca_data['timestamp'] = ''
            try:
                orca_data['last seen'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                orca_data['last seen'] = ''
            orca_data['last fetch time'] = ''
            orca_data['unread'] = ''
            orca_data['unread count'] = entry[1]
            orca_data['unseen count'] = entry[2]
            orca_data['participants'] = ''
            orca_data['former participants'] = ''
            orca_data['senders'] = ''
            orca_data['action id'] = ''
            orca_data['last action id'] = entry[4]

            orca_threads_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from folders table to orca_data
    if folders_data:
        for entry in folders_data:
            orca_data['Table'] = 'folders'
            orca_data['folder'] = entry[0]
            orca_data['thread'] = entry[1]
            orca_data['thread id'] = ''
            orca_data['FaceBook id'] = ''
            orca_data['first name'] = ''
            orca_data['last name'] = ''
            orca_data['name'] = ''
            try:
                orca_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.))
            except TypeError:
                orca_data['timestamp'] = ''
            orca_data['last seen'] = ''
            orca_data['last fetch time'] = ''
            orca_data['unread'] = ''
            orca_data['unread count'] = ''
            orca_data['unseen count'] = ''
            orca_data['participants'] = ''
            orca_data['former participants'] = ''
            orca_data['senders'] = ''
            orca_data['action id'] = ''
            orca_data['last action id'] = ''

            orca_threads_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from thread_users table to orca_data
    if thread_users_data:
        for entry in thread_users_data:
            orca_data['Table'] = 'threads_users'
            orca_data['folder'] = ''
            orca_data['thread'] = ''
            orca_data['thread id'] = ''
            orca_data['FaceBook id'] = entry[0]
            orca_data['first name'] = entry[1]
            orca_data['last name'] = entry[2]
            orca_data['name'] = entry[3]
            orca_data['timestamp'] = ''
            orca_data['last seen'] = ''
            orca_data['last fetch time'] = ''
            orca_data['unread'] = ''
            orca_data['unread count'] = ''
            orca_data['unseen count'] = ''
            orca_data['participants'] = ''
            orca_data['former participants'] = ''
            orca_data['senders'] = ''
            orca_data['action id'] = ''
            orca_data['last action id'] = ''

            orca_threads_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from threads table to orca_data
    if threads_data:
        for entry in threads_data:
            orca_data['Table'] = 'threads'
            orca_data['folder'] = entry[10]
            orca_data['thread'] = entry[0]
            orca_data['thread id'] = entry[1]
            orca_data['FaceBook id'] = ''
            orca_data['first name'] = ''
            orca_data['last name'] = ''
            orca_data['name'] = entry[3]
            try:
                orca_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[7] / 1000.))
            except TypeError:
                orca_data['timestamp'] = ''
            orca_data['last seen'] = ''
            try:
                orca_data['last fetch time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[8] / 1000.))
            except TypeError:
                orca_data['last fetch time'] = ''
            orca_data['unread'] = entry[9]
            orca_data['unread count'] = ''
            orca_data['unseen count'] = ''
            orca_data['participants'] = entry[4]
            orca_data['former participants'] = entry[5]
            orca_data['senders'] = entry[6]
            orca_data['action id'] = entry[2]
            orca_data['last action id'] = ''

            orca_threads_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from threads_db2 database to orca_msg_list
    # Add data from messages table to orca_data
    if messages_data:
        for entry in messages_data:
            orca_data['Table'] = 'messages'
            orca_data['thread'] = entry[1]
            orca_data['text'] = entry[3]
            orca_data['sender'] = entry[4]
            try:
                orca_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                orca_data['timestamp'] = ''
            try:
                orca_data['timestamp sent'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[6] / 1000.))
            except TypeError:
                orca_data['timestamp sent'] = ''
            orca_data['msg id'] = entry[0]
            orca_data['source'] = entry[10]
            orca_data['attachments'] = entry[7]
            orca_data['coordinates'] = entry[8]
            orca_data['offline thread id'] = entry[9]
            orca_data['action id'] = entry[2]
            orca_data['send error'] = entry[11]
            orca_data['send error msg'] = entry[12]

            orca_msg_list.append(orca_data)
            orca_data = OrderedDict()

    return orca_contacts_list, orca_threads_list, orca_msg_list
