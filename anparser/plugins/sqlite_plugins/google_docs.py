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
__date__ = '20150109'
__version__ = '0.00'

from ingest import sqlite_processor  # , time_processor


def google_docs(file_list):
    """
    Parses database folder from com.google.android.apps.docs

    :param file_list: List of all files
    :return: Dictionary of parsed data from DocList.db
    """
    # Initialize table variables: account, collection, contains, entry
    account_data = None
    collection_data = None
    contains_data = None
    entry_data = None

    for file_path in file_list:
        if file_path.endswith(u'DocList.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            views = sqlite_processor.get_sqlite_view_names(file_path)
            if u'Account101' in tables:
                account_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Account101',
                    u'Account_id, accountHolderName, lastSyncTime')
                if account_data is not None:
                    account_data.lastSyncTime = time_processor.unix_time(account_data.lastSyncTime)

            if u'CollectionView' in views:
                collection_data = sqlite_processor.read_sqlite_table(
                    file_path, u'CollectionView',
                    u'_id, Entry_id, title, creator, owner, creationTime, '
                    u'lastModifiedTime, lastModifierAccountAlias, '
                    u'lastModifierAccountName, lastOpenedTime, sharedWithMeTime, '
                    u'shareableByOwner, shared, modifiedByMeTime, mimetype, kind, '
                    u'canEdit, starred, archived, trashed, pinned, accountId, '
                    u'Collection_id, entry_Id')
                if collection_data is not None:
                    collection_data.creationTime = time_processor.unix_time(collection_data.creationTime)
                    collection_data.lastModifiedTime = time_processor.unix_time(collection_data.lastModifiedTime)
                    collection_data.lastOpenedTime = time_processor.unix_time(collection_data.lastOpenedTime)
                    collection_data.sharedWithMeTime = time_processor.unix_time(collection_data.sharedWithMeTime)
                    collection_data.modifiedByMeTime = time_processor.unix_time(collection_data.modifiedByMeTime)

            if u'ContainsId101' in tables:
                contains_data = sqlite_processor.read_sqlite_table(
                    file_path, u'ContainsId101',
                    u'entryId, collectionId')

            if u'EntryView' in views:
                entry_data = sqlite_processor.read_sqlite_table(
                    file_path, u'EntryView',
                    u'Entry_id, title, creator, owner, creationTime, '
                    u'lastModifiedTime, lastModifierAccountAlias, '
                    u'lastModifierAccountName, lastOpenedTime, sharedWithMeTime, '
                    u'shareableByOwner, shared, modifiedByMeTime, mimeType, '
                    u'kind, canEdit, starred, archived, trashed, pinned, accountId, '
                    u'md5Checksum, size')
                if entry_data is not None:
                    entry_data.creationTime = time_processor.unix_time(entry_data.creationTime)
                    entry_data.lastModifiedTime = time_processor.unix_time(entry_data.lastModifiedTime)
                    entry_data.lastOpenedTime = time_processor.unix_time(entry_data.lastOpenedTime)
                    entry_data.sharedWithMeTime = time_processor.unix_time(entry_data.sharedWithMeTime)
                    entry_data.modifiedByMeTime = time_processor.unix_time(entry_data.modifiedByMeTime)

    return account_data, collection_data, contains_data, entry_data