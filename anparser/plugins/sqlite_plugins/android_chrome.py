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
__date__ = '20150112'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import datetime


def android_chrome(file_list):
    """
    Parses chrome databases from com.android.chrome

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # Initialize table variables: Cookies, Downloads, Keywords, Urls, Visits
    cookies_database = None
    history_database = None
    cookies_data = None
    downloads_data = None
    keywords_data = None
    urls_data = None
    visits_data = None

    for file_path in file_list:
        if file_path.endswith('Cookies'):
            cookies_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'cookies' in tables:
                try:
                    cookies_data = __init__.read_sqlite_table(
                        file_path, 'cookies',
                        columns='creation_utc, host_key, name, value, path, expires_utc,'
                                'last_access_utc')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
        if file_path.endswith('History') and file_path.count('app_chrome/Default/History') > 0:
            history_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)
            if 'downloads' in tables:
                try:
                    downloads_data = __init__.read_sqlite_table(
                        file_path, 'downloads',
                        columns='id, current_path, target_path, start_time, '
                                'received_bytes, total_bytes, interrupt_reason, '
                                'end_time, opened, referrer, last_modified, '
                                'mime_type, original_mime_type')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'keyword_search_terms' in tables:
                try:
                    keywords_data = __init__.read_sqlite_table(
                        file_path, 'keyword_search_terms',
                        columns='keyword_id, url_id, lower_term, term')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'urls' in tables:
                try:
                    urls_data = __init__.read_sqlite_table(
                        file_path, 'urls',
                        columns='id, url, title, visit_count, typed_count, last_visit_time,'
                                'hidden')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'visits' in tables:
                try:
                    visits_data = __init__.read_sqlite_table(
                        file_path, 'visits',
                        columns='id, url, visit_time, visit_duration')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    chrome_cookies_list = []
    chrome_downloads_list = []
    chrome_history_list = []
    chrome_data = OrderedDict()

    # Add data from Cookies database to chrome_cookies_list
    # Add data from cookies table to chrome_data
    if cookies_data:
        for entry in cookies_data:
            chrome_data['Database'] = cookies_database
            chrome_data['Table'] = 'cookies'
            chrome_data['Host Key'] = entry['host_key']
            chrome_data['Name'] = entry['name']
            chrome_data['Value'] = entry['value']
            chrome_data['Path'] = entry['path']
            chrome_data['Created UTC'] = chrome_time(entry['creation_utc'])
            chrome_data['Last Accessed UTC'] = chrome_time(entry['last_access_utc'])
            chrome_data['Expires UTC'] = chrome_time(entry['expires_utc'])

            chrome_cookies_list.append(chrome_data)
            chrome_data = OrderedDict()

    # Add data from History database to chrome_downloads_list
    # Add data from downloads table to chrome_data
    if downloads_data:
        for entry in downloads_data:
            chrome_data['Database'] = history_database
            chrome_data['Table'] = 'downloads'
            chrome_data['Download Id'] = entry['id']
            chrome_data['Current Path'] = entry['current_path']
            chrome_data['Target Path'] = entry['target_path']
            chrome_data['Start Time'] = chrome_time(entry['start_time'])
            chrome_data['Received Bytes'] = entry['received_bytes']
            chrome_data['Total Bytes'] = entry['total_bytes']
            chrome_data['Interrupt Reason'] = entry['interrupt_reason']
            chrome_data['End Time'] = chrome_time(entry['end_time'])
            chrome_data['Opened'] = entry['opened']
            chrome_data['Referrer'] = entry['referrer']
            chrome_data['Last Modified'] = entry['last_modified']
            chrome_data['Mime Type'] = entry['mime_type']
            chrome_data['Original Mime Type'] = entry['original_mime_type']

            chrome_downloads_list.append(chrome_data)
            chrome_data = OrderedDict()

    # Add data from History database to chrome_history_list
    # Add data from keyword_search_terms table to chrome_data
    if keywords_data:
        for entry in keywords_data:
            chrome_data['Database'] = history_database
            chrome_data['Table'] = 'keyword_search_terms'
            chrome_data['Keyword Id'] = entry['keyword_id']
            chrome_data['Url Id'] = entry['url_id']
            chrome_data['Visit Id'] = ''
            chrome_data['Lower Search Term'] = entry['lower_term']
            chrome_data['Search Term'] = entry['term']
            chrome_data['Url'] = ''
            chrome_data['Title'] = ''
            chrome_data['Visit Count'] = ''
            chrome_data['Typed Count'] = ''
            chrome_data['Visit Time'] = ''
            chrome_data['Last Visit Time'] = ''
            chrome_data['Visit Duration (Seconds)'] = ''
            chrome_data['Hidden'] = ''

            chrome_history_list.append(chrome_data)
            chrome_data = OrderedDict()

    # Add data from urls table to chrome_data
    if urls_data:
        for entry in urls_data:
            chrome_data['Database'] = history_database
            chrome_data['Table'] = 'urls'
            chrome_data['Keyword Id'] = ''
            chrome_data['Url Id'] = entry['id']
            chrome_data['Visit Id'] = ''
            chrome_data['Lower Search Term'] = ''
            chrome_data['Search Term'] = ''
            chrome_data['Url'] = entry['url']
            chrome_data['Title'] = entry['title']
            chrome_data['Visit Count'] = entry['visit_count']
            chrome_data['Typed Count'] = entry['typed_count']
            chrome_data['Visit Time'] = ''
            chrome_data['Last Visit Time'] = chrome_time(entry['last_visit_time'])
            chrome_data['Visit Duration (Seconds)'] = ''
            chrome_data['Hidden'] = entry['hidden']

            chrome_history_list.append(chrome_data)
            chrome_data = OrderedDict()

    # Add data from visits table to chrome_data
    if visits_data:
        for entry in visits_data:
            chrome_data['Database'] = history_database
            chrome_data['Table'] = 'visits'
            chrome_data['Keyword Id'] = ''
            chrome_data['Url Id'] = entry['url']
            chrome_data['Visit Id'] = entry['id']
            chrome_data['Lower Search Term'] = ''
            chrome_data['Search Term'] = ''
            chrome_data['Url'] = ''
            chrome_data['Title'] = ''
            chrome_data['Visit Count'] = ''
            chrome_data['Typed Count'] = ''
            chrome_data['Visit Time'] = chrome_time(entry['visit_time'])
            chrome_data['Last Visit Time'] = ''
            try:
                chrome_data['Visit Duration (Seconds)'] = entry['visit_duration'] * (1*10**-6)
            except TypeError:
                chrome_data['Visit Duration (Seconds))'] = ''
            chrome_data['Hidden'] = ''

            chrome_history_list.append(chrome_data)
            chrome_data = OrderedDict()

    return chrome_cookies_list, chrome_downloads_list, chrome_history_list


def chrome_time(timestamp):
    """
    Converts Chrome (webkit) time.

    :param timestamp: A webkit timestamp
    :return: A datetime timestamp in format: Y-m-d H:M:S
    """
    offset = 11644473600000
    temp = int(((timestamp / 1000) - offset) * (1*10**-3))
    try:
        dt = datetime.datetime.utcfromtimestamp(temp)
    except (ValueError, TypeError):
        try:
            dt = datetime.datetime.utcfromtimestamp(temp*-1)
        except (ValueError, TypeError):
            dt = None

    try:
        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        timestamp = ''

    return timestamp