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
    contacts_data = None
    folder_counts_data = None
    folders_data = None
    messages_data = None
    thread_users_data = None
    threads_data = None
    notification_data = None

    for file_path in file_list:
        if file_path.endswith('contacts_db2') and file_path.count('com.facebook.katana') > 0:
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
            katana_data['Table'] = 'contacts'
            katana_data['id'] = entry[0]
            katana_data['contact id'] = entry[1]
            katana_data['FaceBook id'] = entry[2]
            katana_data['first name'] = entry[3]
            katana_data['last name'] = entry[4]
            katana_data['name'] = entry[5]

            katana_contacts_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from threads_db2 database to katana_threads_list
    # Add data from folder_counts table to katana_data
    if folder_counts_data:
        for entry in folder_counts_data:
            katana_data['Table'] = 'folder_counts'
            katana_data['folder'] = entry[0]
            katana_data['thread'] = ''
            katana_data['thread id'] = ''
            katana_data['FaceBook id'] = ''
            katana_data['first name'] = ''
            katana_data['last name'] = ''
            katana_data['name'] = ''
            katana_data['timestamp'] = ''
            try:
                katana_data['last seen'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                katana_data['last seen'] = ''
            katana_data['last fetch time'] = ''
            katana_data['unread'] = ''
            katana_data['unread count'] = entry[1]
            katana_data['unseen count'] = entry[2]
            katana_data['participants'] = ''
            katana_data['former participants'] = ''
            katana_data['senders'] = ''
            katana_data['action id'] = ''
            katana_data['last action id'] = entry[4]

            katana_threads_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from folders table to katana_data
    if folders_data:
        for entry in folders_data:
            katana_data['Table'] = 'folders'
            katana_data['folder'] = entry[0]
            katana_data['thread'] = entry[1]
            katana_data['thread id'] = ''
            katana_data['FaceBook id'] = ''
            katana_data['first name'] = ''
            katana_data['last name'] = ''
            katana_data['name'] = ''
            try:
                katana_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.))
            except TypeError:
                katana_data['timestamp'] = ''
            katana_data['last seen'] = ''
            katana_data['last fetch time'] = ''
            katana_data['unread'] = ''
            katana_data['unread count'] = ''
            katana_data['unseen count'] = ''
            katana_data['participants'] = ''
            katana_data['former participants'] = ''
            katana_data['senders'] = ''
            katana_data['action id'] = ''
            katana_data['last action id'] = ''

            katana_threads_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from thread_users table to katana_data
    if thread_users_data:
        for entry in thread_users_data:
            katana_data['Table'] = 'threads_users'
            katana_data['folder'] = ''
            katana_data['thread'] = ''
            katana_data['thread id'] = ''
            katana_data['FaceBook id'] = entry[0]
            katana_data['first name'] = entry[1]
            katana_data['last name'] = entry[2]
            katana_data['name'] = entry[3]
            katana_data['timestamp'] = ''
            katana_data['last seen'] = ''
            katana_data['last fetch time'] = ''
            katana_data['unread'] = ''
            katana_data['unread count'] = ''
            katana_data['unseen count'] = ''
            katana_data['participants'] = ''
            katana_data['former participants'] = ''
            katana_data['senders'] = ''
            katana_data['action id'] = ''
            katana_data['last action id'] = ''

            katana_threads_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from threads table to katana_data
    if threads_data:
        for entry in threads_data:
            katana_data['Table'] = 'threads'
            katana_data['folder'] = entry[10]
            katana_data['thread'] = entry[0]
            katana_data['thread id'] = entry[1]
            katana_data['FaceBook id'] = ''
            katana_data['first name'] = ''
            katana_data['last name'] = ''
            katana_data['name'] = entry[3]
            try:
                katana_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[7] / 1000.))
            except TypeError:
                katana_data['timestamp'] = ''
            katana_data['last seen'] = ''
            try:
                katana_data['last fetch time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[8] / 1000.))
            except TypeError:
                katana_data['last fetch time'] = ''
            katana_data['unread'] = entry[9]
            katana_data['unread count'] = ''
            katana_data['unseen count'] = ''
            katana_data['participants'] = entry[4]
            katana_data['former participants'] = entry[5]
            katana_data['senders'] = entry[6]
            katana_data['action id'] = entry[2]
            katana_data['last action id'] = ''

            katana_threads_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from threads_db2 database to katana_msg_list
    # Add data from messages table to katana_data
    import simplejson
    if messages_data:
        for entry in messages_data:
            katana_data['Table'] = 'messages'
            katana_data['thread'] = entry[1]
            try:
                katana_data['text'] = entry[3].strip('\n')
            except AttributeError:
                katana_data['text'] = entry[3]

            try:
                tmp_dict = simplejson.loads(entry[4].encode('utf-8'))
                katana_data['email'] = tmp_dict['email']
                katana_data['FaceBook id'] = tmp_dict['user_key']
                katana_data['name'] = tmp_dict['name']
            except AttributeError:
                katana_data['email'] = ''
                katana_data['FaceBook id'] = ''
                katana_data['name'] = ''

            try:
                katana_data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                katana_data['timestamp'] = ''
            try:
                katana_data['timestamp sent'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[6] / 1000.))
            except TypeError:
                katana_data['timestamp sent'] = ''
            katana_data['msg id'] = entry[0]
            katana_data['source'] = entry[10]
            if len(entry[7]) < 0:
                katana_data['attachment'] = simplejson.loads(entry[7].encode('utf-8'))[0]['filename']
                katana_data['attachment_url'] = simplejson.loads(entry[7].encode('utf-8'))[0]['urls']['FULL_SCREEN'][
                    'src']
            else:
                katana_data['attachment'] = ''
                katana_data['attachment_url'] = ''
            try:
                tmp_dict = simplejson.loads(entry[8].encode('utf-8'))
                katana_data['latitude'] = tmp_dict['latitude']
                katana_data['logitude'] = tmp_dict['longitude']
                katana_data['accuracy'] = tmp_dict['accuracy']
            except AttributeError:
                katana_data['latitude'] = ''
                katana_data['logitude'] = ''
                katana_data['accuracy'] = ''
            katana_data['offline thread id'] = entry[9]
            katana_data['action id'] = entry[2]
            katana_data['send error'] = entry[11]
            katana_data['send error msg'] = entry[12]

            katana_msg_list.append(katana_data)
            katana_data = OrderedDict()

    # Add data from notifications_db database to katana_notification_list
    # Add data from gql_notification table to katana_data
    if notification_data:
        for entry in notification_data:
            katana_data['Table'] = 'gql_notification'
            katana_data['id'] = entry[0]
            katana_data['notification id'] = entry[1]
            katana_data['recipient FaceBook id'] = entry[2]
            katana_data['seen state'] = entry[3]
            try:
                katana_data['updated'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4]))
            except TypeError:
                katana_data['updated'] = ''
            try:
                tmp_dict = simplejson.loads(str(entry[6]).encode('utf-8'))
                try:
                    katana_data['text'] = tmp_dict['attachments'][0]['description']['text']
                except KeyError:
                    katana_data['text'] = ''
                try:
                    katana_data['sender FaceBook id'] = tmp_dict['actors'][0]['id']
                except KeyError:
                    katana_data['sender FaceBook id'] = ''
                try:
                    katana_data['sender name'] = tmp_dict['actors'][0]['name']
                except KeyError:
                    katana_data['sender name'] = ''
                try:
                    katana_data['creation time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                 time.gmtime(tmp_dict['creation_time']))
                except (TypeError, KeyError):
                    katana_data['creation time'] = ''
            except AttributeError:
                katana_data['text'] = ''
                katana_data['sender FaceBook id'] = ''
                katana_data['sender name'] = ''
                katana_data['creation time'] = ''
            katana_data['cache id'] = entry[5]
            katana_data['profile picture uri'] = entry[7]
            katana_data['photo uri'] = entry[8]

            katana_notification_list.append(katana_data)
            katana_data = OrderedDict()

    return katana_contacts_list, katana_threads_list, katana_msg_list, katana_notification_list