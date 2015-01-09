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
import sqlite_plugins
import time


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
        if file_path.endswith('DocList.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            views = sqlite_plugins.get_sqlite_veiw_info(file_path)
            if 'Account101' in tables:
                try:
                    account_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'Account101',
                        columns='Account_id, accountHolderName, lastSyncTime')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'CollectionView' in views:
                try:
                    collection_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'CollectionView',
                        columns='_id, Entry_id, title, creator, owner, creationTime, '
                                'lastModifiedTime, lastModifierAccountAlias, '
                                'lastModifierAccountName, lastOpenedTime, sharedWithMeTime, '
                                'shareableByOwner, shared, modifiedByMeTime, mimetype, kind, '
                                'canEdit, starred, archived, trashed, pinned, accountId, '
                                'Collection_id, entry_Id')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'ContainsId101' in tables:
                try:
                    contains_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'ContainsId101',
                        columns='entryId, collectionId')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'EntryView' in views:
                try:
                    entry_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'EntryView',
                        columns='Entry_id, title, creator, owner, creationTime, '
                                'lastModifiedTime, lastModifierAccountAlias, '
                                'lastModifierAccountName, lastOpenedTime, sharedWithMeTime, '
                                'shareableByOwner, shared, modifiedByMeTime, mimeType, '
                                'kind, canEdit, starred, archived, trashed, pinned, accountId, '
                                'md5Checksum, size')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    google_docs_account_list = []
    google_docs_collection_list = []
    google_docs_data = OrderedDict()

    # Add data from DocList.db database
    # Add data from Account101 table to google_docs_data
    if account_data:
        for entry in account_data:
            google_docs_data['Table'] = 'Account101'
            google_docs_data['account id'] = entry[0]
            google_docs_data['account Name'] = entry[1]
            try:
                google_docs_data['last sync time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.))
            except TypeError:
                google_docs_data['last sync time'] = ''

            google_docs_account_list.append(google_docs_data)
            google_docs_data = OrderedDict()

    # Add data from ContainsId101 table to google_docs_data
    if contains_data:
        for entry in contains_data:
            google_docs_data['Table'] = 'ContainsId101'
            google_docs_data['collection id'] = entry[1]
            google_docs_data['entry id'] = entry[0]
            google_docs_data['title'] = ''
            google_docs_data['creator'] = ''
            google_docs_data['owner'] = ''
            google_docs_data['account id'] = ''
            google_docs_data['md5 checksum'] = ''
            google_docs_data['size'] = ''
            google_docs_data['creation time'] = ''
            google_docs_data['last modified time'] = ''
            google_docs_data['last modifier account alias'] = ''
            google_docs_data['last modifier account name'] = ''
            google_docs_data['last opened time'] = ''
            google_docs_data['shared with me time'] = ''
            google_docs_data['shareable by owner'] = ''
            google_docs_data['shared'] = ''
            google_docs_data['modified by me time'] = ''
            google_docs_data['mimetype'] = ''
            google_docs_data['kind'] = ''
            google_docs_data['can edit'] = ''
            google_docs_data['starred'] = ''
            google_docs_data['archived'] = ''
            google_docs_data['trashed'] = ''
            google_docs_data['pinned'] = ''

            google_docs_collection_list.append(google_docs_data)
            google_docs_data = OrderedDict()

    # Add data from CollectionView table to google_docs_data
    if collection_data:
        for entry in collection_data:
            google_docs_data['Table'] = 'CollectionView'
            google_docs_data['collection id'] = entry[22]
            google_docs_data['entry id'] = entry[1]
            google_docs_data['title'] = entry[2]
            google_docs_data['creator'] = entry[3]
            google_docs_data['owner'] = entry[4]
            google_docs_data['account id'] = entry[21]
            google_docs_data['md5 checksum'] = ''
            google_docs_data['size'] = ''
            try:
                google_docs_data['creation time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                google_docs_data['creation time'] = ''
            try:
                google_docs_data['last modified time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[6] / 1000.))
            except TypeError:
                google_docs_data['last modified time'] = ''
            google_docs_data['last modifier account alias'] = entry[7]
            google_docs_data['last modifier account name'] = entry[8]
            try:
                google_docs_data['last opened time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[9] / 1000.))
            except TypeError:
                google_docs_data['last opened time'] = ''
            try:
                google_docs_data['shared with me time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[10] / 1000.))
            except TypeError:
                google_docs_data['shared with me time'] = ''
            google_docs_data['shareable by owner'] = entry[11]
            google_docs_data['shared'] = entry[12]
            try:
                google_docs_data['modified by me time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[13] / 1000.))
            except TypeError:
                google_docs_data['modified by me time'] = ''
            google_docs_data['mimetype'] = entry[14]
            google_docs_data['kind'] = entry[15]
            google_docs_data['can edit'] = entry[16]
            google_docs_data['starred'] = entry[17]
            google_docs_data['archived'] = entry[18]
            google_docs_data['trashed'] = entry[19]
            google_docs_data['pinned'] = entry[20]

            google_docs_collection_list.append(google_docs_data)
            google_docs_data = OrderedDict()

    # Add data from EntryView table to google_docs_data
    if entry_data:
        for entry in entry_data:
            google_docs_data['Table'] = 'EntryView'
            google_docs_data['collection id'] = ''
            google_docs_data['entry id'] = entry[0]
            google_docs_data['title'] = entry[1]
            google_docs_data['creator'] = entry[2]
            google_docs_data['owner'] = entry[3]
            google_docs_data['account id'] = entry[20]
            google_docs_data['md5 checksum'] = entry[21]
            google_docs_data['size'] = entry[22]
            try:
                google_docs_data['creation time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.))
            except TypeError:
                google_docs_data['creation time'] = ''
            try:
                google_docs_data['last modified time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                google_docs_data['last modified time'] = ''
            google_docs_data['last modifier account alias'] = entry[6]
            google_docs_data['last modifier account name'] = entry[7]
            try:
                google_docs_data['last opened time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[8] / 1000.))
            except TypeError:
                google_docs_data['last opened time'] = ''
            try:
                google_docs_data['shared with me time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[9] / 1000.))
            except TypeError:
                google_docs_data['shared with me time'] = ''
            google_docs_data['shareable by owner'] = entry[10]
            google_docs_data['shared'] = entry[11]
            try:
                google_docs_data['modified by me time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(entry[12] / 1000.))
            except TypeError:
                google_docs_data['modified by me time'] = ''
            google_docs_data['mimetype'] = entry[13]
            google_docs_data['kind'] = entry[14]
            google_docs_data['can edit'] = entry[15]
            google_docs_data['starred'] = entry[16]
            google_docs_data['archived'] = entry[17]
            google_docs_data['trashed'] = entry[18]
            google_docs_data['pinned'] = entry[19]

            google_docs_collection_list.append(google_docs_data)
            google_docs_data = OrderedDict()

    return google_docs_account_list, google_docs_collection_list