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

from ingest import sqlite_processor, time_processor


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
        if file_path.endswith(u'Cookies') and file_path.count(u'com.android.chrome') > 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'cookies' in tables:
                cookies_data = sqlite_processor.read_sqlite_table(
                    file_path, u'cookies', u'creation_utc, host_key, name, value, '
                                            u'path, expires_utc, last_access_utc')
                if cookies_data is not None:
                    cookies_data.creation_utc = time_processor.chrome_time(cookies_data.creation_utc)
                    cookies_data.expires_utc = time_processor.chrome_time(cookies_data.expires_utc)
                    cookies_data.last_access_utc = time_processor.chrome_time(cookies_data.last_access_utc)

        if file_path.endswith(u'History') and file_path.count(u'app_chrome/Default/History') > 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'downloads' in tables:
                downloads_data = sqlite_processor.read_sqlite_table(
                    file_path, u'downloads', u'id, current_path, target_path, start_time, '
                                              u'received_bytes, total_bytes, interrupt_reason, '
                                              u'end_time, opened, referrer, last_modified, '
                                              u'mime_type, original_mime_type')
                if downloads_data is not None:
                    downloads_data.start_time = time_processor.chrome_time(downloads_data.start_time)
                    downloads_data.end_time = time_processor.chrome_time(downloads_data.end_time)

            if u'keyword_search_terms' in tables:
                keywords_data = sqlite_processor.read_sqlite_table(
                    file_path, u'keyword_search_terms', u'keyword_id, url_id, lower_term, term')

            if u'urls' in tables:
                urls_data = sqlite_processor.read_sqlite_table(
                    file_path, u'urls', u'id, url, title, visit_count, typed_count, last_visit_time, hidden')
                if urls_data is not None:
                    urls_data.last_visit_time = time_processor.chrome_time(urls_data.last_visit_time)

            if u'visits' in tables:
                visits_data = sqlite_processor.read_sqlite_table(
                    file_path, u'visits', u'id, url, visit_time, visit_duration')
                if visits_data is not None:
                    visits_data.visit_time = time_processor.chrome_time(visits_data.visit_time)

    return cookies_data, downloads_data, keywords_data, urls_data, visits_data