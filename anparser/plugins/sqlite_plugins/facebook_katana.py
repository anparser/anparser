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
__date__ = '20150113'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import time


def facebook_katana(file_list):
    """
    Parses database folder from com.facebook.katana

    :param file_list: List of all files
    :return: Dictionary of parsed data from databases
    """
    # TODO: Add support for group_conversations table in threads_db2.
    # Initialize table variables: contacts, folder_counts, folders, messages, thread_users, threads, gql_notifications
    contacts_database = None
    threads_database = None
    notification_database = None
    contacts_data = None
    folder_counts_data = None
    folders_data = None
    messages_data = None
    thread_users_data = None
    threads_data = None
    notification_data = None

    for file_path in file_list:
        if file_path.endswith('contacts_db2') and file_path.count('com.facebook.katana') > 0:
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
        if file_path.endswith('threads_db2') and file_path.count('com.facebook.katana') > 0:
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
        if file_path.endswith('notifications_db') and file_path.count('com.facebook.katana') > 0:
            notification_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'gql_notifications' in tables:
                try:
                    notification_data = __init__.read_sqlite_table(
                        file_path, 'gql_notifications',
                        columns='_id, notif_id, recipient_id, seen_state, updated, cache_id, '
                                'gql_payload, profile_picture_uri, photo_uri')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    katana_contacts_list = []
    katana_msg_list = []
    katana_threads_list = []
    katana_notification_list = []
    katana_data = OrderedDict()

    # Add data from contacts_db2 database to katana_contacts_list
    # Add data from contacts table to katana_data
    if contacts_data:
        for entry in contacts_data:
            katana_data['Database'] = contacts_database
            katana_data['Table'] = 'contacts'
            katana_data['Id'] = entry[0]
            katana_data['Contact Id'] = entry[1]
            katana_data['FaceBook Id'] = entry[2]
            katana_data['First Name'] = entry[3]
            katana_data['Last Name'] = entry[4]
            katana_data['Name'] = entry[5]

            katana_contacts_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from threads_db2 database to katana_threads_list
    # Add data from folder_counts table to katana_data
    if folder_counts_data:
        for entry in folder_counts_data:
            katana_data['Database'] = threads_database
            katana_data['Table'] = 'folder_counts'
            katana_data['Folder'] = entry[0]
            katana_data['Thread'] = ''
            katana_data['Thread Id'] = ''
            katana_data['FaceBook Id'] = ''
            katana_data['First Name'] = ''
            katana_data['Last Name'] = ''
            katana_data['Name'] = ''
            katana_data['Timestamp'] = ''
            try:
                katana_data['Last Seen'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                katana_data['Last Seen'] = ''
            katana_data['Last Fetch Time'] = ''
            katana_data['Unread'] = ''
            katana_data['Unread Count'] = entry[1]
            katana_data['Unseen Count'] = entry[2]
            katana_data['Participants'] = ''
            katana_data['Former Participants'] = ''
            katana_data['Senders'] = ''
            katana_data['Action Id'] = ''
            katana_data['Last Action Id'] = entry[4]

            katana_threads_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from folders table to katana_data
    if folders_data:
        for entry in folders_data:
            katana_data['Database'] = threads_database
            katana_data['Table'] = 'folders'
            katana_data['Folder'] = entry[0]
            katana_data['Thread'] = entry[1]
            katana_data['Thread Id'] = ''
            katana_data['FaceBook Id'] = ''
            katana_data['First Name'] = ''
            katana_data['Last Name'] = ''
            katana_data['Name'] = ''
            try:
                katana_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.))
            except TypeError:
                katana_data['Timestamp'] = ''
            katana_data['Last Seen'] = ''
            katana_data['Last Fetch Time'] = ''
            katana_data['Unread'] = ''
            katana_data['Unread Count'] = ''
            katana_data['Unseen Count'] = ''
            katana_data['Participants'] = ''
            katana_data['Former Participants'] = ''
            katana_data['Senders'] = ''
            katana_data['Action Id'] = ''
            katana_data['Last Action Id'] = ''

            katana_threads_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from thread_users table to katana_data
    if thread_users_data:
        for entry in thread_users_data:
            katana_data['Database'] = threads_database
            katana_data['Table'] = 'threads_users'
            katana_data['Folder'] = ''
            katana_data['Thread'] = ''
            katana_data['Thread Id'] = ''
            katana_data['FaceBook Id'] = entry[0]
            katana_data['First Name'] = entry[1]
            katana_data['Last Name'] = entry[2]
            katana_data['Name'] = entry[3]
            katana_data['Timestamp'] = ''
            katana_data['Last Seen'] = ''
            katana_data['Last Fetch Time'] = ''
            katana_data['Unread'] = ''
            katana_data['Unread Count'] = ''
            katana_data['Unseen Count'] = ''
            katana_data['Participants'] = ''
            katana_data['Former Participants'] = ''
            katana_data['Senders'] = ''
            katana_data['Action Id'] = ''
            katana_data['Last Action Id'] = ''

            katana_threads_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from threads table to katana_data
    if threads_data:
        for entry in threads_data:
            katana_data['Database'] = threads_database
            katana_data['Table'] = 'threads'
            katana_data['Folder'] = entry[10]
            katana_data['Thread'] = entry[0]
            katana_data['Thread Id'] = entry[1]
            katana_data['FaceBook Id'] = ''
            katana_data['First Name'] = ''
            katana_data['Last Name'] = ''
            katana_data['Name'] = entry[3]
            try:
                katana_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[7] / 1000.))
            except TypeError:
                katana_data['Timestamp'] = ''
            katana_data['Last Seen'] = ''
            try:
                katana_data['Last Fetch Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[8] / 1000.))
            except TypeError:
                katana_data['Last Fetch Time'] = ''
            katana_data['Unread'] = entry[9]
            katana_data['Unread Count'] = ''
            katana_data['Unseen Count'] = ''
            katana_data['Participants'] = entry[4]
            katana_data['Former Participants'] = entry[5]
            katana_data['Senders'] = entry[6]
            katana_data['Action Id'] = entry[2]
            katana_data['Last Action Id'] = ''

            katana_threads_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from threads_db2 database to katana_msg_list
    # Add data from messages table to katana_data
    import simplejson
    if messages_data:
        for entry in messages_data:
            katana_data['Database'] = threads_database
            katana_data['Table'] = 'messages'
            katana_data['Thread'] = entry[1]
            try:
                katana_data['Text'] = entry[3].strip('\n')
            except AttributeError:
                katana_data['Text'] = entry[3]

            try:
                tmp_dict = simplejson.loads(entry[4].encode('utf-8'))
                katana_data['Email'] = tmp_dict['email']
                katana_data['FaceBook Id'] = tmp_dict['user_key']
                katana_data['Name'] = tmp_dict['name']
            except AttributeError:
                katana_data['Email'] = ''
                katana_data['FaceBook Id'] = ''
                katana_data['Name'] = ''

            try:
                katana_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                katana_data['Timestamp'] = ''
            try:
                katana_data['Timestamp Sent'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[6] / 1000.))
            except TypeError:
                katana_data['Timestamp Sent'] = ''
            katana_data['Message Id'] = entry[0]
            katana_data['Source'] = entry[10]
            if len(entry[7]) < 0:
                katana_data['Attachment'] = simplejson.loads(entry[7].encode('utf-8'))[0]['filename']
                katana_data['Attachment Url'] = simplejson.loads(entry[7].encode('utf-8'))[0]['urls']['FULL_SCREEN'][
                    'src']
            else:
                katana_data['Attachment'] = ''
                katana_data['Attachment Url'] = ''
            try:
                tmp_dict = simplejson.loads(entry[8].encode('utf-8'))
                katana_data['Latitude'] = tmp_dict['latitude']
                katana_data['Longitude'] = tmp_dict['longitude']
                katana_data['Accuracy'] = tmp_dict['accuracy']
            except AttributeError:
                katana_data['Latitude'] = ''
                katana_data['Longitude'] = ''
                katana_data['Accuracy'] = ''
            katana_data['Offline Thread Id'] = entry[9]
            katana_data['Action Id'] = entry[2]
            katana_data['Send Error'] = entry[11]
            katana_data['Send Error Message'] = entry[12]

            katana_msg_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from notifications_db database to katana_notification_list
    # Add data from gql_notification table to katana_data
    if notification_data:
        for entry in notification_data:
            katana_data['Database'] = notification_database
            katana_data['Table'] = 'gql_notification'
            katana_data['Id'] = entry[0]
            katana_data['Notification Id'] = entry[1]
            katana_data['Recipient FaceBook Id'] = entry[2]
            katana_data['Seen State'] = entry[3]
            try:
                katana_data['Updated'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4]))
            except TypeError:
                katana_data['Updated'] = ''
            try:
                tmp_dict = simplejson.loads(str(entry[6]).encode('utf-8'))
                try:
                    katana_data['Text'] = tmp_dict['attachments'][0]['description']['text']
                except KeyError:
                    katana_data['Text'] = ''
                try:
                    katana_data['Sender FaceBook Id'] = tmp_dict['actors'][0]['id']
                except KeyError:
                    katana_data['Sender FaceBook Id'] = ''
                try:
                    katana_data['Sender Name'] = tmp_dict['actors'][0]['name']
                except KeyError:
                    katana_data['Sender Name'] = ''
                try:
                    katana_data['Creation Time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                 time.gmtime(tmp_dict['creation_time']))
                except (TypeError, KeyError):
                    katana_data['Creation Time'] = ''
            except AttributeError:
                katana_data['Text'] = ''
                katana_data['Sender FaceBook Id'] = ''
                katana_data['Sender Name'] = ''
                katana_data['Creation Time'] = ''
            katana_data['Cache Id'] = entry[5]
            katana_data['Profile Picture Uri'] = entry[7]
            katana_data['Photo Uri'] = entry[8]

            katana_notification_list.append(katana_data)
            katana_data = OrderedDict()

    return katana_contacts_list, katana_threads_list, katana_msg_list, katana_notification_list