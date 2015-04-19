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
__date__ = '20150221'
__version__ = '0.00'

from ingest import sqlite_processor, time_processor


def infraware_office(file_list):
    """
    Parses databases from database folder in com.infraware.office.link

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables:
    contacts_data = None
    files_data = None
    attendee_data = None
    group_data = None
    share_data = None
    message_data = None

    for file_path in file_list:
        if file_path.endswith(u'InfrawarePoLinkContacts.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'PoLinkFriend' in tables:
                contacts_data = sqlite_processor.read_sqlite_table(
                    file_path, u'PoLinkFriend',
                    u'ID, NAME, EMAIL, USER_ID, LAST_SEND_TIME')
                if contacts_data is not None:
                    contacts_data.LAST_SEND_TIME = time_processor.unix_time(contacts_data.LAST_SEND_TIME, 1)
                    contacts_data['Database Path'] = file_path


        if file_path.endswith(u'InfrawarePoLinkFiles.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'PoLinkFiles' in tables:
                files_data = sqlite_processor.read_sqlite_table(
                    file_path, u'PoLinkFiles',
                    u'_id, fileId, fileName, fileExt, lastRevision, lastModified, fileType, parentId, size, '
                    u'lastAccessTime, path, shared, deletedTime, lastModifiedRevision, isSyncronized, isMyFile, '
                    u'md5, referenceId, lastFileRevision, sharedRevision, originalId')
                if files_data is not None:
                    files_data.lastModified = time_processor.unix_time(files_data.lastModified)
                    files_data.lastAccessTime = time_processor.unix_time(files_data.lastAccessTime)
                    files_data.deletedTime = time_processor.unix_time(files_data.deletedTime)
                    files_data['Database Path'] = file_path

        if file_path.endswith(u'InfrawarePoLinkMessages.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'ATTENDEE' in tables:
                attendee_data = sqlite_processor.read_sqlite_table(
                    file_path, u'ATTENDEE',
                    u'ATTENDEE_ID, ATTENDEE_NAME, EMAIL, LAST_INVITE_SEND_TIME, GROUP_ID')
                if attendee_data is not None:
                    attendee_data.LAST_INVITE_SEND_TIME = time_processor.unix_time(
                        attendee_data.LAST_INVITE_SEND_TIME, 1)
                    attendee_data['Database Path'] = file_path

            if u'GROUP_LIST' in tables:
                group_data = sqlite_processor.read_sqlite_table(
                    file_path, u'GROUP_LIST',
                    u'GROUP_ID, NEW_MESSAGE_COUNT, GROUP_NAME, LAST_MSG_ID, ATTENDEE_COUNT')
                if group_data is not None:
                    group_data['Database Path'] = file_path

            if u'SHARE_LIST' in tables:
                share_data = sqlite_processor.read_sqlite_table(
                    file_path, u'SHARE_LIST',
                    u'SHARE_ID, SHARE_OWNER_ID, SHARE_OWNER_NAME, SHARE_OWNER_EMAIL, SHARE_GROUP_ID, '
                    u'SHARE_CREATE_TIME, FILE_ID, FILE_NAME, FILE_LAST_REVISION, FILE_LAST_MODIFIED_TIME, FILE_SIZE')
                if share_data is not None:
                    share_data.SHARE_CREATE_TIME = time_processor.unix_time(share_data.SHARE_CREATE_TIME, 1)
                    share_data.FILE_LAST_MODIFIED_TIME = time_processor.unix_time(share_data.FILE_LAST_MODIFIED_TIME, 1)
                    share_data['Database Path'] = file_path

            if u'MESSAGE' in tables:
                message_data = sqlite_processor.read_sqlite_table(
                    file_path, u'MESSAGE',
                    u'MESSAGE_ID, GROUP_ID, MESSAGE_TYPE, DATA, EDITOR_ID, EDITOR_NAME, TIME, SYSTEM_MESSAGE_ACTOR_ID, '
                    u'SYSTEM_MESSAGE_ACTOR_EMAIL')
                if message_data is not None:
                    message_data.TIME = time_processor.unix_time(message_data.TIME, 1)
                    message_data['Database Path'] = file_path

    return contacts_data, files_data, attendee_data, share_data, message_data