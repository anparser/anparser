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

from collections import OrderedDict
import logging
import __init__
import time


def google_docs(file_list):
    """
    Parses database folder from com.google.android.apps.docs

    :param file_list: List of all files
    :return: Dictionary of parsed data from DocList.db
    """
    # Initialize table variables: account, collection, contains, entry
    doclist_database = None
    account_data = None
    collection_data = None
    contains_data = None
    entry_data = None

    for file_path in file_list:
        if file_path.endswith('DocList.db'):
            doclist_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            views = __init__.get_sqlite_veiw_info(file_path)
            if 'Account101' in tables:
                try:
                    account_data = __init__.read_sqlite_table(
                        file_path, 'Account101',
                        columns='Account_id, accountHolderName, lastSyncTime')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'CollectionView' in views:
                try:
                    collection_data = __init__.read_sqlite_table(
                        file_path, 'CollectionView',
                        columns='_id, Entry_id, title, creator, owner, creationTime, '
                                'lastModifiedTime, lastModifierAccountAlias, '
                                'lastModifierAccountName, lastOpenedTime, sharedWithMeTime, '
                                'shareableByOwner, shared, modifiedByMeTime, mimetype, kind, '
                                'canEdit, starred, archived, trashed, pinned, accountId, '
                                'Collection_id, entry_Id')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'ContainsId101' in tables:
                try:
                    contains_data = __init__.read_sqlite_table(
                        file_path, 'ContainsId101',
                        columns='entryId, collectionId')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'EntryView' in views:
                try:
                    entry_data = __init__.read_sqlite_table(
                        file_path, 'EntryView',
                        columns='Entry_id, title, creator, owner, creationTime, '
                                'lastModifiedTime, lastModifierAccountAlias, '
                                'lastModifierAccountName, lastOpenedTime, sharedWithMeTime, '
                                'shareableByOwner, shared, modifiedByMeTime, mimeType, '
                                'kind, canEdit, starred, archived, trashed, pinned, accountId, '
                                'md5Checksum, size')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    google_docs_account_list = []
    google_docs_collection_list = []
    google_docs_data = OrderedDict()

    # Add data from DocList.db database
    # Add data from Account101 table to google_docs_data
    if account_data:
        for entry in account_data:
            google_docs_data['Database'] = doclist_database
            google_docs_data['Table'] = 'Account101'
            google_docs_data['Account Id'] = entry['Account_id']
            google_docs_data['Account Name'] = entry['accountHolderName']
            try:
                google_docs_data['Last Sync Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['lastSyncTime'] / 1000.))
            except TypeError:
                google_docs_data['Last Sync Time'] = ''

            google_docs_account_list.append(google_docs_data)
            google_docs_data = OrderedDict()

    # Add data from ContainsId101 table to google_docs_data
    if contains_data:
        for entry in contains_data:
            google_docs_data['Database'] = doclist_database
            google_docs_data['Table'] = 'ContainsId101'
            google_docs_data['Collection Id'] = entry['collectionId']
            google_docs_data['Entry Id'] = entry['entryId']
            google_docs_data['Title'] = ''
            google_docs_data['Creator'] = ''
            google_docs_data['Owner'] = ''
            google_docs_data['Account Id'] = ''
            google_docs_data['md5 Checksum'] = ''
            google_docs_data['Size'] = ''
            google_docs_data['Creation Time'] = ''
            google_docs_data['Last Modified Time'] = ''
            google_docs_data['Last Modifier Account Alias'] = ''
            google_docs_data['Last Modifier Account Name'] = ''
            google_docs_data['Last Opened Time'] = ''
            google_docs_data['Shared With Me Time'] = ''
            google_docs_data['Shareable By Owner'] = ''
            google_docs_data['Shared'] = ''
            google_docs_data['Modified By Me Time'] = ''
            google_docs_data['Mime Type'] = ''
            google_docs_data['Kind'] = ''
            google_docs_data['Can Edit'] = ''
            google_docs_data['Starred'] = ''
            google_docs_data['Archived'] = ''
            google_docs_data['Trashed'] = ''
            google_docs_data['Pinned'] = ''

            google_docs_collection_list.append(google_docs_data)
            google_docs_data = OrderedDict()

    # Add data from CollectionView table to google_docs_data
    if collection_data:
        for entry in collection_data:
            google_docs_data['Database'] = doclist_database
            google_docs_data['Table'] = 'CollectionView'
            google_docs_data['Collection Id'] = entry['Collection_id']
            google_docs_data['Entry Id'] = entry['Entry_id']
            google_docs_data['Title'] = entry['title']
            google_docs_data['Creator'] = entry['creator']
            google_docs_data['Owner'] = entry['owner']
            google_docs_data['Account Id'] = entry['accountId']
            google_docs_data['md5 Checksum'] = ''
            google_docs_data['Size'] = ''
            try:
                google_docs_data['Creation Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['creationTime'] / 1000.))
            except TypeError:
                google_docs_data['Creation Time'] = ''
            try:
                google_docs_data['Last Modified Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['lastModifiedTime'] / 1000.))
            except TypeError:
                google_docs_data['Last Modified Time'] = ''
            google_docs_data['Last Modifier Account Alias'] = entry['lastModifierAccountAlias']
            google_docs_data['Last Modifier Account Name'] = entry['lastModifierAccountName']
            try:
                google_docs_data['Last Opened Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['lastOpenedTime'] / 1000.))
            except TypeError:
                google_docs_data['Last Opened Time'] = ''
            try:
                google_docs_data['Shared With Me Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['sharedWithMeTime'] / 1000.))
            except TypeError:
                google_docs_data['Shared With Me Time'] = ''
            google_docs_data['Shareable By Owner'] = entry['shareableByOwner']
            google_docs_data['Shared'] = entry['shared']
            try:
                google_docs_data['Modified By Me Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['modifiedByMeTime'] / 1000.))
            except TypeError:
                google_docs_data['Modified By Me Time'] = ''
            google_docs_data['Mime Type'] = entry['mimetype']
            google_docs_data['Kind'] = entry['kind']
            google_docs_data['Can Edit'] = entry['canEdit']
            google_docs_data['Starred'] = entry['starred']
            google_docs_data['Archived'] = entry['archived']
            google_docs_data['Trashed'] = entry['trashed']
            google_docs_data['Pinned'] = entry['pinned']

            google_docs_collection_list.append(google_docs_data)
            google_docs_data = OrderedDict()

    # Add data from EntryView table to google_docs_data
    if entry_data:
        for entry in entry_data:
            google_docs_data['Database'] = doclist_database
            google_docs_data['Table'] = 'EntryView'
            google_docs_data['Collection Id'] = ''
            google_docs_data['Entry Id'] = entry['Entry_id']
            google_docs_data['Title'] = entry['title']
            google_docs_data['Creator'] = entry['creator']
            google_docs_data['Owner'] = entry['owner']
            google_docs_data['Account Id'] = entry['accountId']
            google_docs_data['md5 Checksum'] = entry['md5Checksum']
            google_docs_data['Size'] = entry['size']
            try:
                google_docs_data['Creation Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['creationTime'] / 1000.))
            except TypeError:
                google_docs_data['Creation Time'] = ''
            try:
                google_docs_data['Last Modified Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['lastModifiedTime'] / 1000.))
            except TypeError:
                google_docs_data['Last Modified Time'] = ''
            google_docs_data['Last Modifier Account Alias'] = entry['lastModifierAccountAlias']
            google_docs_data['Last Modifier Account Name'] = entry['lastModifierAccountName']
            try:
                google_docs_data['Last Opened Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['lastOpenedTime'] / 1000.))
            except TypeError:
                google_docs_data['Last Opened Time'] = ''
            try:
                google_docs_data['Shared With Me Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['sharedWithMeTime'] / 1000.))
            except TypeError:
                google_docs_data['Shared With Me Time'] = ''
            google_docs_data['Shareable By Owner'] = entry['shareableByOwner']
            google_docs_data['Shared'] = entry['shared']
            try:
                google_docs_data['Modified By Me Time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry['modifiedByMeTime'] / 1000.))
            except TypeError:
                google_docs_data['Modified By Me Time'] = ''
            google_docs_data['Mime Type'] = entry['mimeType']
            google_docs_data['Kind'] = entry['kind']
            google_docs_data['Can Edit'] = entry['canEdit']
            google_docs_data['Starred'] = entry['starred']
            google_docs_data['Archived'] = entry['archived']
            google_docs_data['Trashed'] = entry['trashed']
            google_docs_data['Pinned'] = entry['pinned']

            google_docs_collection_list.append(google_docs_data)
            google_docs_data = OrderedDict()

    return google_docs_account_list, google_docs_collection_list