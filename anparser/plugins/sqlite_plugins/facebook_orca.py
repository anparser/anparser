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

from collections import OrderedDict
import logging
import __init__
import time


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
        if file_path.endswith('contacts_db2') and file_path.count('com.facebook.orca') > 0:
            contacts_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'contacts' in tables:
                try:
                    contacts_data = __init__.read_sqlite_table(
                        file_path, 'contacts',
                        columns='internal_id, contact_id, fbid, first_name, last_name, '
                                'display_name')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('threads_db2') and file_path.count('com.facebook.orca') > 0:
            threads_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'folder_counts' in tables:
                try:
                    folder_counts_data = __init__.read_sqlite_table(
                        file_path, 'folder_counts',
                        columns='folder, unread_count, unseen_count, last_seen_time, last_action_id')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'folders' in tables:
                try:
                    folders_data = __init__.read_sqlite_table(
                        file_path, 'folders',
                        columns='folder, thread_key, timestamp_ms')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'messages' in tables:
                try:
                    messages_data = __init__.read_sqlite_table(
                        file_path, 'messages',
                        columns='msg_id, thread_key, action_id, text, sender, timestamp_ms, '
                                'timestamp_sent_ms, attachments, coordinates, offline_threading_id, '
                                'source, send_error, send_error_message')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'thread_users' in tables:
                thread_users_data = __init__.read_sqlite_table(
                    file_path, 'thread_users',
                    columns='user_key, first_name, last_name, name')
            if 'threads' in tables:
                try:
                    threads_data = __init__.read_sqlite_table(
                        file_path, 'threads',
                        columns='thread_key, thread_fbid, action_id, name, '
                                'participants, former_participants, senders, '
                                'timestamp_ms, last_fetch_time_ms, unread, '
                                'folder')
                except __init__.sqlite3.OperationalError as exception:
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
            orca_data['Database'] = contacts_database
            orca_data['Table'] = 'contacts'
            orca_data['Id'] = entry[0]
            orca_data['Contact Id'] = entry[1]
            orca_data['FaceBook Id'] = entry[2]
            orca_data['First Name'] = entry[3]
            orca_data['Last Name'] = entry[4]
            orca_data['Name'] = entry[5]

            orca_contacts_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from threads_db2 database to orca_threads_list
    # Add data from folder_counts table to orca_data
    if folder_counts_data:
        for entry in folder_counts_data:
            orca_data['Database'] = threads_database
            orca_data['Table'] = 'folder_counts'
            orca_data['Folder'] = entry[0]
            orca_data['Thread'] = ''
            orca_data['Thread Id'] = ''
            orca_data['FaceBook Id'] = ''
            orca_data['First Name'] = ''
            orca_data['Last Name'] = ''
            orca_data['Name'] = ''
            orca_data['Timestamp'] = ''
            try:
                orca_data['Last Seen'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                orca_data['Last Seen'] = ''
            orca_data['Last Fetch Time'] = ''
            orca_data['Unread'] = ''
            orca_data['Unread Count'] = entry[1]
            orca_data['Unseen Count'] = entry[2]
            orca_data['Participants'] = ''
            orca_data['Former Participants'] = ''
            orca_data['Senders'] = ''
            orca_data['Action Id'] = ''
            orca_data['Last Action Id'] = entry[4]

            orca_threads_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from folders table to orca_data
    if folders_data:
        for entry in folders_data:
            orca_data['Database'] = threads_database
            orca_data['Table'] = 'folders'
            orca_data['Folder'] = entry[0]
            orca_data['Thread'] = entry[1]
            orca_data['Thread Id'] = ''
            orca_data['FaceBook Id'] = ''
            orca_data['First Name'] = ''
            orca_data['Last Name'] = ''
            orca_data['Name'] = ''
            try:
                orca_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.))
            except TypeError:
                orca_data['Timestamp'] = ''
            orca_data['Last Seen'] = ''
            orca_data['Last Fetch Time'] = ''
            orca_data['Unread'] = ''
            orca_data['Unread Count'] = ''
            orca_data['Unseen Count'] = ''
            orca_data['Participants'] = ''
            orca_data['Former Participants'] = ''
            orca_data['Senders'] = ''
            orca_data['Action Id'] = ''
            orca_data['Last Action Id'] = ''

            orca_threads_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from thread_users table to orca_data
    if thread_users_data:
        for entry in thread_users_data:
            orca_data['Database'] = threads_database
            orca_data['Table'] = 'threads_users'
            orca_data['Folder'] = ''
            orca_data['Thread'] = ''
            orca_data['Thread Id'] = ''
            orca_data['FaceBook Id'] = entry[0]
            orca_data['First Name'] = entry[1]
            orca_data['Last Name'] = entry[2]
            orca_data['Name'] = entry[3]
            orca_data['Timestamp'] = ''
            orca_data['Last Seen'] = ''
            orca_data['Last Fetch Time'] = ''
            orca_data['Unread'] = ''
            orca_data['Unread Count'] = ''
            orca_data['Unseen Count'] = ''
            orca_data['Participants'] = ''
            orca_data['Former Participants'] = ''
            orca_data['Senders'] = ''
            orca_data['Action Id'] = ''
            orca_data['Last Action Id'] = ''

            orca_threads_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from threads table to orca_data
    if threads_data:
        for entry in threads_data:
            orca_data['Database'] = threads_database
            orca_data['Table'] = 'threads'
            orca_data['Folder'] = entry[10]
            orca_data['Thread'] = entry[0]
            orca_data['Thread Id'] = entry[1]
            orca_data['FaceBook Id'] = ''
            orca_data['First Name'] = ''
            orca_data['Last Name'] = ''
            orca_data['Name'] = entry[3]
            try:
                orca_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[7] / 1000.))
            except TypeError:
                orca_data['Timestamp'] = ''
            orca_data['Last Seen'] = ''
            try:
                orca_data['Last Fetch Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[8] / 1000.))
            except TypeError:
                orca_data['Last Fetch Time'] = ''
            orca_data['Unread'] = entry[9]
            orca_data['Unread Count'] = ''
            orca_data['Unseen Count'] = ''
            orca_data['Participants'] = entry[4]
            orca_data['Former Participants'] = entry[5]
            orca_data['Senders'] = entry[6]
            orca_data['Action Id'] = entry[2]
            orca_data['Last Action Id'] = ''

            orca_threads_list.append(orca_data)
            orca_data = OrderedDict()

    # Add data from threads_db2 database to orca_msg_list
    # Add data from messages table to orca_data
    import simplejson
    if messages_data:
        for entry in messages_data:
            orca_data['Database'] = threads_database
            orca_data['Table'] = 'messages'
            orca_data['Thread'] = entry[1]
            try:
                orca_data['Text'] = entry[3].strip('\n')
            except AttributeError:
                orca_data['Text'] = entry[3]

            try:
                tmp_dict = simplejson.loads(entry[4].encode('utf-8'))
                orca_data['Email'] = tmp_dict['email']
                orca_data['FaceBook Id'] = tmp_dict['user_key']
                orca_data['Name'] = tmp_dict['name']
            except AttributeError:
                orca_data['Email'] = ''
                orca_data['FaceBook Id'] = ''
                orca_data['Name'] = ''

            try:
                orca_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                orca_data['Timestamp'] = ''
            try:
                orca_data['Timestamp Sent'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[6] / 1000.))
            except TypeError:
                orca_data['Timestamp Sent'] = ''
            orca_data['Message Id'] = entry[0]
            orca_data['Source'] = entry[10]
            if len(entry[7]) < 0:
                orca_data['Attachment'] = simplejson.loads(entry[7].encode('utf-8'))[0]['filename']
                orca_data['Attachment Url'] = simplejson.loads(entry[7].encode('utf-8'))[0]['urls']['FULL_SCREEN'][
                    'src']
            else:
                orca_data['Attachment'] = ''
                orca_data['Attachment Url'] = ''
            try:
                tmp_dict = simplejson.loads(entry[8].encode('utf-8'))
                orca_data['Latitude'] = tmp_dict['latitude']
                orca_data['Longitude'] = tmp_dict['longitude']
                orca_data['Accuracy'] = tmp_dict['accuracy']
            except AttributeError:
                orca_data['Latitude'] = ''
                orca_data['Longitude'] = ''
                orca_data['Accuracy'] = ''
            orca_data['Offline Thread Id'] = entry[9]
            orca_data['Action Id'] = entry[2]
            orca_data['Send Error'] = entry[11]
            orca_data['Send Error Message'] = entry[12]

            orca_msg_list.append(orca_data)
            orca_data = OrderedDict()

    return orca_contacts_list, orca_threads_list, orca_msg_list