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
__date__ = '20150118'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import time


def snapchat_android(file_list):
    """
    Parses tcspahn.db database from com.snapchat.android

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: Chat, Conversation, Friends, MyStoriesFiles, ReceivedSnaps, SentSnaps,
    # SnapImageFiles, SnapVideoFiles, ViewingSessions
    tcspahn_database = None
    chat_data = None
    conversation_data = None
    friends_data = None
    storyfiles_data = None
    recvsnaps_data = None
    sentsnaps_data = None
    image_files_data = None
    video_files_data = None
    viewing_sessions_data = None

    for file_path in file_list:
        if file_path.endswith('tcspahn.db'):
            tcspahn_database = file_path
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'Chat' in tables:
                try:
                    chat_data = __init__.read_sqlite_table(
                        file_path, 'Chat',
                        columns='_id, recipient, sender, is_saved_by_sender, is_saved_by_recipient, '
                                'send_receive_status, timestamp, text, conversation_id')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'Conversation' in tables:
                try:
                    conversation_data = __init__.read_sqlite_table(
                        file_path, 'Conversation',
                        columns='_id, sender, recipient, timestamp, has_unviewed_snaps, '
                                'has_unviewed_chats')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'Friends' in tables:
                try:
                    friends_data = __init__.read_sqlite_table(
                        file_path, 'Friends',
                        columns='_id, Username, DisplayName, PhoneNumber, AddedMeTimestamp, '
                                'AddedThemTimestamp')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'MyStoriesFiles' in tables:
                try:
                    storyfiles_data = __init__.read_sqlite_table(
                        file_path, 'MyStoriesFiles',
                        columns='_id, SnapId, FilePath')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'ReceivedSnaps' in tables:
                try:
                    recvsnaps_data = __init__.read_sqlite_table(
                        file_path, 'ReceivedSnaps',
                        columns='_id, Timestamp, Status, Sender, IsViewed, IsScreenshotted, '
                                'ViewedTimestamp, ConversationId, SentTimestamp')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'SentSnaps' in tables:
                try:
                    sentsnaps_data = __init__.read_sqlite_table(
                        file_path, 'SentSnaps',
                        columns='_id, Timestamp, Status, Recipient, '
                                'ConversationId, SentTimestamp')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'SnapImageFiles' in tables:
                try:
                    image_files_data = __init__.read_sqlite_table(
                        file_path, 'SnapImageFiles',
                        columns='_id, SnapId, FilePath')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'SnapVideoFiles' in tables:
                try:
                    video_files_data = __init__.read_sqlite_table(
                        file_path, 'SnapVideoFiles',
                        columns='_id, SnapId, FilePath')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'ViewingSessions' in tables:
                try:
                    viewing_sessions_data = __init__.read_sqlite_table(
                        file_path, 'ViewingSessions',
                        columns='_id, Sender, StartTime, EndTime, Type, Extra')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    snapchat_friends_list = []
    snapchat_chat_list = []
    snapchat_viewing_list = []
    snapchat_files_list = []
    snapchat_data = OrderedDict()

    # Add tables from tcspahn.db to snapchat_friends_list
    # Add data from Friends table to snapchat_data
    if friends_data:
        for entry in friends_data:
            snapchat_data['Database'] = tcspahn_database
            snapchat_data['Table'] = 'Friends'
            snapchat_data['Id'] = entry[0]
            snapchat_data['Username'] = entry[1]
            snapchat_data['Display Name'] = entry[2]
            snapchat_data['Phone Number'] = entry[3]
            try:
                snapchat_data['Added Me Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.))
            except TypeError:
                snapchat_data['Added Me Timestamp'] = ''
            try:
                snapchat_data['Added Them Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                snapchat_data['Added Them Timestamp'] = ''

            snapchat_friends_list.append(snapchat_data)
            snapchat_data = OrderedDict()

    # Add data from tcspahn.db to snapchat_chat_list
    # Add data from Chat table to snapchat_data
    if chat_data:
        for entry in chat_data:
            snapchat_data['Database'] = tcspahn_database
            snapchat_data['Table'] = 'Chat'
            snapchat_data['Chat Id'] = entry[0]
            snapchat_data['Conversation Id'] = entry[8]
            snapchat_data['ReceivedSnaps Id'] = ''
            snapchat_data['SentSnaps Id'] = ''
            snapchat_data['Sender'] = entry[2]
            snapchat_data['Recipient'] = entry[1]
            snapchat_data['Status'] = entry[5]
            snapchat_data['Text'] = entry[7]
            try:
                snapchat_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[6] / 1000.))
            except TypeError:
                snapchat_data['Timestamp'] = ''
            snapchat_data['Viewed Timestamp'] = ''
            snapchat_data['Sent Timestamp'] = ''
            snapchat_data['Is Viewed'] = ''
            snapchat_data['Is Screenshotted'] = ''
            snapchat_data['Is Saved By Sender'] = entry[3]
            snapchat_data['Is Saved By Recipient'] = entry[4]
            snapchat_data['Has Unviewed Snaps'] = ''
            snapchat_data['Has Unviewed Chats'] = ''

            snapchat_chat_list.append(snapchat_data)
            snapchat_data = OrderedDict()

    # Add data from Conversation table to snapchat_data
    if conversation_data:
        for entry in conversation_data:
            snapchat_data['Database'] = tcspahn_database
            snapchat_data['Table'] = 'Conversation'
            snapchat_data['Chat Id'] = ''
            snapchat_data['Conversation Id'] = entry[0]
            snapchat_data['ReceivedSnaps Id'] = ''
            snapchat_data['SentSnaps Id'] = ''
            snapchat_data['Sender'] = entry[1]
            snapchat_data['Recipient'] = entry[2]
            snapchat_data['Status'] = ''
            snapchat_data['Text'] = ''
            try:
                snapchat_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                snapchat_data['Timestamp'] = ''
            snapchat_data['Viewed Timestamp'] = ''
            snapchat_data['Sent Timestamp'] = ''
            snapchat_data['Is Viewed'] = ''
            snapchat_data['Is Screenshotted'] = ''
            snapchat_data['Is Saved By Sender'] = ''
            snapchat_data['Is Saved By Recipient'] = ''
            snapchat_data['Has Unviewed Snaps'] = entry[4]
            snapchat_data['Has Unviewed Chats'] = entry[5]

            snapchat_chat_list.append(snapchat_data)
            snapchat_data = OrderedDict()

    # Add data from ReceivedSnaps table to snapchat_data
    if recvsnaps_data:
        for entry in recvsnaps_data:
            snapchat_data['Database'] = tcspahn_database
            snapchat_data['Table'] = 'ReceivedSnaps'
            snapchat_data['Chat Id'] = ''
            snapchat_data['Conversation Id'] = entry[7]
            snapchat_data['ReceivedSnaps Id'] = entry[0]
            snapchat_data['SentSnaps Id'] = ''
            snapchat_data['Sender'] = entry[3]
            snapchat_data['Recipient'] = ''
            snapchat_data['Status'] = entry[2]
            snapchat_data['Text'] = ''
            try:
                snapchat_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[1] / 1000.))
            except TypeError:
                snapchat_data['Timestamp'] = ''
            try:
                snapchat_data['Viewed Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[6] / 1000.))
            except TypeError:
                snapchat_data['Viewed Timestamp'] = ''
            try:
                snapchat_data['Sent Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[8] / 1000.))
            except TypeError:
                snapchat_data['Sent Timestamp'] = ''
            snapchat_data['Is Viewed'] = entry[4]
            snapchat_data['Is Screenshotted'] = entry[5]
            snapchat_data['Is Saved By Sender'] = ''
            snapchat_data['Is Saved By Recipient'] = ''
            snapchat_data['Has Unviewed Snaps'] = ''
            snapchat_data['Has Unviewed Chats'] = ''

            snapchat_chat_list.append(snapchat_data)
            snapchat_data = OrderedDict()

    # Add data from SentSnaps table to snapchat_data
    if sentsnaps_data:
        for entry in sentsnaps_data:
            snapchat_data['Database'] = tcspahn_database
            snapchat_data['Table'] = 'SentSnaps'
            snapchat_data['Chat Id'] = ''
            snapchat_data['Conversation Id'] = entry[4]
            snapchat_data['ReceivedSnaps Id'] = ''
            snapchat_data['SentSnaps Id'] = entry[0]
            snapchat_data['Sender'] = ''
            snapchat_data['Recipient'] = entry[3]
            snapchat_data['Status'] = entry[2]
            snapchat_data['Text'] = ''
            try:
                snapchat_data['Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[1] / 1000.))
            except TypeError:
                snapchat_data['Timestamp'] = ''
            snapchat_data['Viewed Timestamp'] = ''
            try:
                snapchat_data['Sent Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                snapchat_data['Sent Timestamp'] = ''
            snapchat_data['Is Viewed'] = ''
            snapchat_data['Is Screenshotted'] = ''
            snapchat_data['Is Saved By Sender'] = ''
            snapchat_data['Is Saved By Recipient'] = ''
            snapchat_data['Has Unviewed Snaps'] = ''
            snapchat_data['Has Unviewed Chats'] = ''

            snapchat_chat_list.append(snapchat_data)
            snapchat_data = OrderedDict()

    # Add data from tcspahn.db to snapchat_viewing_list
    # Add data from ViewingSessions table to snapchat_data
    if viewing_sessions_data:
        for entry in viewing_sessions_data:
            snapchat_data['Database'] = tcspahn_database
            snapchat_data['Table'] = 'ViewingSessions'
            snapchat_data['ViewingSessions Id'] = entry[0]
            snapchat_data['Sender'] = entry[1]
            snapchat_data['Type'] = entry[4]
            snapchat_data['Extra'] = entry[5]
            try:
                snapchat_data['Start Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.))
            except TypeError:
                snapchat_data['Start Time'] = ''
            try:
                snapchat_data['End Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                snapchat_data['End Time'] = ''

            snapchat_viewing_list.append(snapchat_data)
            snapchat_data = OrderedDict()

    # Add data from tcspahn.db to snapchat_files_list
    # Add data from MyStoriesFiles table to snapchat_data
    if storyfiles_data:
        for entry in storyfiles_data:
            snapchat_data['Database'] = tcspahn_database
            snapchat_data['Table'] = 'MyStoriesFiles'
            snapchat_data['MyStoriesFiles Id'] = entry[0]
            snapchat_data['SnapImagesFiles Id'] = ''
            snapchat_data['SnapVideoFiles Id'] = ''
            snapchat_data['Snap Id'] = entry[1]
            snapchat_data['File Path'] = entry[2]

            snapchat_files_list.append(snapchat_data)
            snapchat_data = OrderedDict()

    # Add data from SnapImageFiles table to snapchat_data
    if image_files_data:
        for entry in image_files_data:
            snapchat_data['Database'] = tcspahn_database
            snapchat_data['Table'] = 'SnapImageFiles'
            snapchat_data['MyStoriesFiles Id'] = ''
            snapchat_data['SnapImagesFiles Id'] = entry[0]
            snapchat_data['SnapVideoFiles Id'] = ''
            snapchat_data['Snap Id'] = entry[1]
            snapchat_data['File Path'] = entry[2]

            snapchat_files_list.append(snapchat_data)
            snapchat_data = OrderedDict()

    # Add data from SnapVideoFiles table to snapchat_data
    if video_files_data:
        for entry in video_files_data:
            snapchat_data['Database'] = tcspahn_database
            snapchat_data['Table'] = 'SnapVideoFiles'
            snapchat_data['MyStoriesFiles Id'] = ''
            snapchat_data['SnapImagesFiles Id'] = ''
            snapchat_data['SnapVideoFiles Id'] = entry[0]
            snapchat_data['Snap Id'] = entry[1]
            snapchat_data['File Path'] = entry[2]

            snapchat_files_list.append(snapchat_data)
            snapchat_data = OrderedDict()

    return snapchat_friends_list, snapchat_chat_list, snapchat_viewing_list, snapchat_files_list