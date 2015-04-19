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
__date__ = '20150212'
__version__ = '0.00'

from ingest import sqlite_processor, time_processor


def venmo(file_list):
    """
    Parses venmo.sqlite from com.venmo

    :param file_list: List of all files
    :return: Dictionary of parsed data from databases
    """
    # Initialize table variables: library, localappstate, suggestions
    comments_data = None
    stories_data = None
    person_data = None
    user_data = None

    for file_path in file_list:
        if file_path.endswith(u'venmo.sqlite'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'comments' in tables:
                comments_data = sqlite_processor.read_sqlite_table(
                    file_path, u'comments', u'_id, comment_id, comment_message, created_time, comment_actor_id, '
                                            u'comment_story_owner, comment_mentions')
                if comments_data is not None:
                    comments_data.created_time = time_processor.unix_time(comments_data.created_time)
                    comments_data['Database Path'] = file_path

            if u'stories' in tables:
                stories_data = sqlite_processor.read_sqlite_table(
                    file_path, u'stories', u'_id, story_id, story_blob, audience, created_time, updated_time, '
                                           u'likes_ids, comment_ids, feed_owners')
                if stories_data is not None:
                    stories_data.created_time = time_processor.unix_time(stories_data.created_time)
                    stories_data.updated_time = time_processor.unix_time(stories_data.updated_time)
                    stories_data['Database Path'] = file_path

            if u'table_person' in tables:
                person_data = sqlite_processor.read_sqlite_table(
                    file_path, u'table_person', u'_id, fullname, firstname, lastname, user_id, external_id, '
                                                u'username, registration_status, phones_list, emails_list, '
                                                u'friend_status')
                if person_data is not None:
                    person_data['Database Path'] = file_path

            if u'users' in tables:
                user_data = sqlite_processor.read_sqlite_table(
                    file_path, u'users', u'_id, user_id, name, username, firstname, lastname, last_accessed, cancelled')
                if user_data is not None:
                    user_data.last_accessed = time_processor.unix_time(user_data.last_accessed)
                    user_data['Database Path'] = file_path

    return comments_data, stories_data, person_data, user_data