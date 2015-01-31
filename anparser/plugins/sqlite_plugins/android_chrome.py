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
import sqlite_processor


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
        if file_path.endswith(u'Cookies'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'cookies' in tables:
                cookies_data = sqlite_processor.read_sqlite_table(
                    file_path, u'cookies', [u'creation_utc', u'host_key', u'name', u'value',
                                            u'path', u'expires_utc', u'last_access_utc'])

        if file_path.endswith(u'History') and file_path.count(u'app_chrome/Default/History') > 0:
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'downloads' in tables:
                downloads_data = sqlite_processor.read_sqlite_table(
                    file_path, u'downloads', [u'id', u'current_path', u'target_path', u'start_time',
                                              u'received_bytes', u'total_bytes', u'interrupt_reason',
                                              u'end_time', u'opened', u'referrer', u'last_modified',
                                              u'mime_type', u'original_mime_type'])

            if u'keyword_search_terms' in tables:
                keywords_data = sqlite_processor.read_sqlite_table(
                    file_path, u'keyword_search_terms', [u'keyword_id', u'url_id', u'lower_term', u'term'])

            if u'urls' in tables:
                urls_data = sqlite_processor.read_sqlite_table(
                    file_path, u'urls', [u'id', u'url', u'title', u'visit_count', u'typed_count',
                                         u'last_visit_time', u'hidden'])

            if u'visits' in tables:
                visits_data = sqlite_processor.read_sqlite_table(
                    file_path, u'visits', [u'id', u'url', u'visit_time', u'visit_duration'])

    return cookies_data, downloads_data, keywords_data, urls_data, visits_data