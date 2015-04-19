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
__date__ = '20150202'
__version__ = '0.00'

from ingest import sqlite_processor, time_processor


def skype_raider(file_list):
    """
    Parses main.db database from com.skype.raider

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """

    # Initialize table variables: contents, tagging, tags
    accounts_data = None
    call_members = None
    call_data = None
    chat_members = None
    chat_data = None
    contacts = None
    conversations = None
    media_documents = None
    messages = None
    participants = None
    transfers = None

    for file_path in file_list:
        if file_path.endswith(u'main.db') and file_path.count(u'com.skype.raider') > 0 and file_path.count(u'qik') == 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)

            if u'Accounts' in tables:
                accounts_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Accounts',
                    u'id, pwdchangestatus, skypeout_balance_currency, registration_timestamp, liveid_membername, '
                    u'owner_under_legal_age, skypename, pstnnumber, fullname, birthday, city, phone_home, '
                    u'phone_office, phone_mobile, homepage, about, profile_timestamp, displayname, mood_text, '
                    u'ipcountry, lastonline_timestamp, avatar_timestamp, mood_timestamp')
                if accounts_data is not None:
                    accounts_data.profile_timestamp = time_processor.unix_time(accounts_data.profile_timestamp, 1)
                    accounts_data.lastonline_timestamp = time_processor.unix_time(accounts_data.lastonline_timestamp, 1)
                    accounts_data.avatar_timestamp = time_processor.unix_time(accounts_data.avatar_timestamp, 1)
                    accounts_data.mood_timestamp = time_processor.unix_time(accounts_data.mood_timestamp, 1)
                    accounts_data['Database Path'] = file_path

            if u'CallMembers' in tables:
                call_members = sqlite_processor.read_sqlite_table(
                    file_path, u'CallMembers',
                    u'id, identity, dispname, call_duration, price_per_minute, call_name, guid, real_identity, '
                    u'start_timestamp, is_conference, creation_timestamp, version_string, ip_address')
                if call_members is not None:
                    call_members.start_timestamp = time_processor.unix_time(call_members.start_timestamp, 1)
                    call_members.creation_timestamp = time_processor.unix_time(call_members.creation_timestamp, 1)
                    call_members['Database Path'] = file_path

            if u'Calls' in tables:
                call_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Calls',
                    u'id, begin_timestamp, host_identity, duration, active_members, name, is_incoming, is_conference, '
                    u'start_timestamp, old_members, conv_dbid')
                if call_data is not None:
                    call_data.begin_timestamp = time_processor.unix_time(call_data.begin_timestamp, 1)
                    call_data.start_timestamp = time_processor.unix_time(call_data.start_timestamp, 1)
                    call_data['Database Path'] = file_path

            if u'ChatMembers' in tables:
                chat_members = sqlite_processor.read_sqlite_table(
                    file_path, u'ChatMembers',
                    u'id, chatname, identity, adder')
                if chat_members is not None:
                    chat_members['Database Path'] = file_path

            if u'Chats' in tables:
                chat_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Chats',
                    u'id, name, friendlyname, timestamp, activity_timestamp, dialog_partner, adder, participants, '
                    u'activemembers, last_change, first_unread_message, dbpath, conv_dbid')
                if chat_data is not None:
                    chat_data.timestamp = time_processor.unix_time(chat_data.timestamp, 1)
                    chat_data.activity_timestamp = time_processor.unix_time(chat_data.activity_timestamp, 1)
                    chat_data.last_change = time_processor.unix_time(chat_data.last_change, 1)
                    chat_data['Database Path'] = file_path

            if u'Contacts' in tables:
                contacts = sqlite_processor.read_sqlite_table(
                    file_path, u'Contacts',
                    u'id, skypename, fullname, birthday, country, city, phone_home, phone_office, phone_mobile, '
                    u'emails, homepage, about, mood_text, profile_timestamp, ipcountry, avatar_timestamp, '
                    u'mood_timestamp, lastonline_timestamp, displayname, lastused_timestamp, main_phone, '
                    u'phone_mobile_normalized')
                if contacts is not None:
                    contacts.profile_timestamp = time_processor.unix_time(contacts.profile_timestamp, 1)
                    contacts.avatar_timestamp = time_processor.unix_time(contacts.avatar_timestamp, 1)
                    contacts.mood_timestamp = time_processor.unix_time(contacts.mood_timestamp, 1)
                    contacts.lastonline_timestamp = time_processor.unix_time(contacts.lastonline_timestamp, 1)
                    contacts.lastused_timestamp = time_processor.unix_time(contacts.lastused_timestamp, 1)
                    contacts['Database Path'] = file_path

            if u'Conversations' in tables:
                conversations = sqlite_processor.read_sqlite_table(
                    file_path, u'Conversations',
                    u'id, identity, live_start_timestamp, is_bookmarked, is_blocked, displayname, inbox_timestamp, '
                    u'inbox_message_id, last_message_id, last_activity_timestamp, creator, creation_timestamp, guid, '
                    u'chat_dbid')
                if conversations is not None:
                    conversations.live_start_timestamp = time_processor.unix_time(conversations.live_start_timestamp, 1)
                    conversations.inbox_timestamp = time_processor.unix_time(conversations.inbox_timestamp, 1)
                    conversations.last_activity_timestamp = time_processor.unix_time(
                        conversations.last_activity_timestamp, 1)
                    conversations.creation_timestamp = time_processor.unix_time(conversations.creation_timestamp, 1)
                    conversations['Database Path'] = file_path

            if u'MediaDocuments' in tables:
                media_documents = sqlite_processor.read_sqlite_table(
                    file_path, u'MediaDocuments',
                    u'id, uri, original_name, title, description, mime_type')
                if media_documents is not None:
                    media_documents['Database Path'] = file_path

            if u'Messages' in tables:
                # TODO: guid column error- look into this. (TypeError: writable buffers are not hashable)
                messages = sqlite_processor.read_sqlite_table(
                    file_path, u'Messages',
                    u'id, chatname, author, from_dispname, dialog_partner, timestamp, edited_by, '
                    u'edited_timestamp, body_xml, participant_count, crc')
                if messages is not None:
                    messages.timestamp = time_processor.unix_time(messages.timestamp, 1)
                    messages.edited_timestamp = time_processor.unix_time(messages.edited_timestamp, 1)

            if u'Participants' in tables:
                participants = sqlite_processor.read_sqlite_table(
                    file_path, u'Participants',
                    u'id, convo_id, identity, live_start_timestamp, adder, live_ip_address, real_identity')
                if participants is not None:
                    participants.live_start_timestamp = time_processor.unix_time(participants.live_start_timestamp)
                    participants['Database Path'] = file_path

            if u'Transfers' in tables:
                # TODO: chatmsg_guid column error - look into this. (TypeError: writable buffers are not hashable)
                transfers = sqlite_processor.read_sqlite_table(
                    file_path, u'Transfers',
                    u'id, partner_handle, partner_dispname, starttime, finishtime, filepath, filename, filesize, '
                    u'convo_id')
                if transfers is not None:
                    transfers.starttime = time_processor.unix_time(transfers.starttime, 1)
                    transfers.finishtime = time_processor.unix_time(transfers.finishtime, 1)
                    transfers['Database Path'] = file_path


    return accounts_data, call_members, call_data, chat_members, chat_data, contacts, conversations,\
           media_documents, messages, participants, transfers