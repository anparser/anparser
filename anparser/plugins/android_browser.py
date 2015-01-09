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
__date__ = '20150107'
__version__ = '0.00'

from collections import OrderedDict
import logging
import sqlite_plugins
import time


def android_browser(file_list):
    """
    Parses browser database from com.android.browser

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # TODO: Add in support for other tables (images, thumbnails).
    # Initialize table variables: bookmarks, history, v_accounts
    bookmarks_data = None
    history_data = None
    accounts_data = None

    for file_path in file_list:
        if file_path.endswith('browser2.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            views = sqlite_plugins.get_sqlite_veiw_info(file_path)
            if 'bookmarks' in tables:
                try:
                    bookmarks_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'bookmarks',
                        columns='_id, title, url, deleted, created, modified')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'history' in tables:
                try:
                    history_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'history',
                        columns='_id, title, url, date, visits')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'v_accounts' in views:
                try:
                    accounts_data = sqlite_plugins.read_sqlite_table(
                        file_path, 'v_accounts',
                        columns='account_name, account_type, root_id')
                except sqlite_plugins.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    browser_data_list = []
    browser_data = OrderedDict()

    # Add data from bookmarks table to browser_data
    if bookmarks_data:
        for entry in bookmarks_data:
            browser_data['Table'] = 'bookmarks'
            browser_data['id'] = entry[0]
            browser_data['title'] = entry[1]
            browser_data['url'] = entry[2]
            browser_data['deleted'] = entry[3]
            try:
                browser_data['created'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.))
            except TypeError:
                browser_data['created'] = ''
            try:
                browser_data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                browser_data['modified'] = ''
            browser_data['date'] = ''
            browser_data['visits'] = ''
            browser_data['account_name'] = ''
            browser_data['account_type'] = ''

            browser_data_list.append(browser_data)
            browser_data = OrderedDict()

    # Add data from history table to browser_data
    if history_data:
        for entry in history_data:
            browser_data['Table'] = 'history'
            browser_data['id'] = entry[0]
            browser_data['title'] = entry[1]
            browser_data['url'] = entry[2]
            browser_data['deleted'] = ''
            browser_data['created'] = ''
            browser_data['modified'] = ''
            try:
                browser_data['date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                browser_data['date'] = ''
            browser_data['visits'] = entry[4]
            browser_data['account_name'] = ''
            browser_data['account_type'] = ''

            browser_data_list.append(browser_data)
            browser_data = OrderedDict()

    # Add data from v_accounts table to browser_data
    if accounts_data:
        for entry in accounts_data:
            browser_data['Table'] = 'v_accounts'
            browser_data['id'] = entry[2]
            browser_data['title'] = ''
            browser_data['url'] = ''
            browser_data['deleted'] = ''
            browser_data['created'] = ''
            browser_data['modified'] = ''
            browser_data['date'] = ''
            browser_data['visits'] = ''
            browser_data['account_name'] = entry[0]
            browser_data['account_type'] = entry[1]

            browser_data_list.append(browser_data)
            browser_data = OrderedDict()

    return browser_data_list
