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

from ingest import sqlite_processor, time_processor


def snapchat_android(file_list):
    """
    Parses tcspahn.db database from com.snapchat.android

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: Chat, Conversation, Friends, MyStoriesFiles, ReceivedSnaps, SentSnaps,
    # SnapImageFiles, SnapVideoFiles, ViewingSessions
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
        if file_path.endswith(u'tcspahn.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'Chat' in tables:
                chat_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Chat',
                    u'_id, recipient, sender, is_saved_by_sender, is_saved_by_recipient, '
                    u'send_receive_status, timestamp, text, conversation_id')
                if chat_data is not None:
                    chat_data.timestamp = time_processor.unix_time(chat_data.timestamp)

            if u'Conversation' in tables:
                conversation_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Conversation',
                    u'_id, sender, recipient, timestamp, has_unviewed_snaps, '
                    u'has_unviewed_chats')
                if conversation_data is not None:
                    conversation_data.timestamp = time_processor.unix_time(conversation_data.timestamp)

            if u'Friends' in tables:
                friends_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Friends',
                    u'_id, Username, DisplayName, PhoneNumber, AddedMeTimestamp, '
                    u'AddedThemTimestamp')
                if friends_data is not None:
                    friends_data.AddedMeTimestamp = time_processor.unix_time(friends_data.AddedMeTimestamp)
                    friends_data.AddedThemTimestamp = time_processor.unix_time(friends_data.AddedThemTimestamp)

            if u'MyStoriesFiles' in tables:
                storyfiles_data = sqlite_processor.read_sqlite_table(
                    file_path, u'MyStoriesFiles',
                    u'_id, SnapId, FilePath')

            if u'ReceivedSnaps' in tables:
                recvsnaps_data = sqlite_processor.read_sqlite_table(
                    file_path, u'ReceivedSnaps',
                    u'_id, Timestamp, Status, Sender, IsViewed, IsScreenshotted, '
                    u'ViewedTimestamp, ConversationId, SentTimestamp')
                if recvsnaps_data is not None:
                    recvsnaps_data.Timestamp = time_processor.unix_time(recvsnaps_data.Timestamp)
                    recvsnaps_data.ViewedTimestamp = time_processor.unix_time(recvsnaps_data.ViewedTimestamp)
                    recvsnaps_data.SentTimestamp = time_processor.unix_time(recvsnaps_data.SentTimestamp)

            if u'SentSnaps' in tables:
                sentsnaps_data = sqlite_processor.read_sqlite_table(
                    file_path, u'SentSnaps',
                    u'_id, Timestamp, Status, Recipient, '
                    u'ConversationId, SentTimestamp')
                if sentsnaps_data is not None:
                    sentsnaps_data.Timestamp = time_processor.unix_time(sentsnaps_data.Timestamp)
                    sentsnaps_data.SentTimestamp = time_processor.unix_time(sentsnaps_data.SentTimestamp)

            if u'SnapImageFiles' in tables:
                image_files_data = sqlite_processor.read_sqlite_table(
                    file_path, u'SnapImageFiles',
                    u'_id, SnapId, FilePath')

            if u'SnapVideoFiles' in tables:
                video_files_data = sqlite_processor.read_sqlite_table(
                    file_path, u'SnapVideoFiles',
                    u'_id, SnapId, FilePath')

            if u'ViewingSessions' in tables:
                viewing_sessions_data = sqlite_processor.read_sqlite_table(
                    file_path, 'ViewingSessions',
                    u'_id, Sender, StartTime, EndTime, Type, Extra')
                if viewing_sessions_data is not None:
                    viewing_sessions_data.StartTime = time_processor.unix_time(viewing_sessions_data.StartTime)
                    viewing_sessions_data.EndTime = time_processor.unix_time(viewing_sessions_data.EndTime)

    return chat_data, conversation_data, friends_data, storyfiles_data, recvsnaps_data, sentsnaps_data,\
           image_files_data, video_files_data, viewing_sessions_data