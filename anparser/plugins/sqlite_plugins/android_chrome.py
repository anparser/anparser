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
    cookies_data = None
    downloads_data = None
    keywords_data = None
    urls_data = None
    visits_data = None

    for file_path in file_list:
        if file_path.endswith('Cookies'):
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
                    print visits_data
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass


    chrome_cookies_list = []
    chrome_downloads_list = []
    chrome_history_list = []
    chrome_data = OrderedDict()
    dt = None

    # Add data from Cookies database to chrome_cookies_list
    # Add data from cookies table to chrome_data
    if cookies_data:
        for entry in cookies_data:
            chrome_data['Table'] = 'cookies'
            chrome_data['host key'] = entry[1]
            chrome_data['name'] = entry[2]
            chrome_data['value'] = entry[3]
            chrome_data['path'] = entry[4]
            chrome_data['created utc'] = chrome_time(entry[0])
            chrome_data['last accessed utc'] = chrome_time(entry[6])
            chrome_data['expires utc'] = chrome_time(entry[5])

            chrome_cookies_list.append(chrome_data)
            chrome_data = OrderedDict()

    # Add data from History database to chrome_downloads_list
    # Add data from downloads table to chrome_data
    if downloads_data:
        for entry in downloads_data:
            chrome_data['Table'] = 'downloads'
            chrome_data['download id'] = entry[0]
            chrome_data['current path'] = entry[1]
            chrome_data['target path'] = entry[2]
            chrome_data['start time'] = chrome_time(entry[3])
            chrome_data['received bytes'] = entry[4]
            chrome_data['total bytes'] = entry[5]
            chrome_data['interrupt reason'] = entry[6]
            chrome_data['end time'] = chrome_time(entry[7])
            chrome_data['opened'] = entry[8]
            chrome_data['referrer'] = entry[9]
            chrome_data['last modified'] = entry[10]
            chrome_data['mime type'] = entry[11]
            chrome_data['original mime type'] = entry[12]

            chrome_downloads_list.append(chrome_data)
            chrome_data = OrderedDict()

    # Add data from History database to chrome_history_list
    # Add data from keyword_search_terms table to chrome_data
    if keywords_data:
        for entry in keywords_data:
            chrome_data['Table'] = 'keyword_search_terms'
            chrome_data['keyword id'] = entry[0]
            chrome_data['url id'] = entry[1]
            chrome_data['visit id'] = ''
            chrome_data['lower search term'] = entry[2]
            chrome_data['search term'] = entry[3]
            chrome_data['url'] = ''
            chrome_data['title'] = ''
            chrome_data['visit count'] = ''
            chrome_data['typed count'] = ''
            chrome_data['visit time'] = ''
            chrome_data['last visit time'] = ''
            chrome_data['visit duration (seconds)'] = ''
            chrome_data['hidden'] = ''

            chrome_history_list.append(chrome_data)
            chrome_data = OrderedDict()

    # Add data from urls table to chrome_data
    if urls_data:
        for entry in urls_data:
            chrome_data['Table'] = 'urls'
            chrome_data['keyword id'] = ''
            chrome_data['url id'] = entry[0]
            chrome_data['visit id'] = ''
            chrome_data['lower search term'] = ''
            chrome_data['search term'] = ''
            chrome_data['url'] = entry[1]
            chrome_data['title'] = entry[2]
            chrome_data['visit count'] = entry[3]
            chrome_data['typed count'] = entry[4]
            chrome_data['visit time'] = ''
            chrome_data['last visit time'] = chrome_time(entry[5])
            chrome_data['visit duration (seconds)'] = ''
            chrome_data['hidden'] = entry[6]

            chrome_history_list.append(chrome_data)
            chrome_data = OrderedDict()

    # Add data from visits table to chrome_data
    if visits_data:
        for entry in visits_data:
            chrome_data['Table'] = 'visits'
            chrome_data['keyword id'] = ''
            chrome_data['url id'] = entry[1]
            chrome_data['visit id'] = entry[0]
            chrome_data['lower search term'] = ''
            chrome_data['search term'] = ''
            chrome_data['url'] = ''
            chrome_data['title'] = ''
            chrome_data['visit count'] = ''
            chrome_data['typed count'] = ''
            chrome_data['visit time'] = chrome_time(entry[2])
            chrome_data['last visit time'] = ''
            try:
                chrome_data['visit duration (seconds)'] = entry[3] * (1*10**-6)
            except TypeError:
                chrome_data['visit duration (seconds)'] = ''
            chrome_data['hidden'] = ''

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
