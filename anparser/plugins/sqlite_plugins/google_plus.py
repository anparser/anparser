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
__date__ = '20150123'
__version__ = '0.00'

from collections import OrderedDict
import datetime
import logging
import __init__
import time


def google_plus(file_list):
    """
    Parses database folder from com.google.android.apps.plus

    :param file_list: List of all files
    :return: Dictionary of parsed data from DocList.db
    """
    # Initialize table variables: all_photos, contact_search, contacts, guns,
    es0_database = None
    photos_data = None
    contact_search_data = None
    contacts_data = None
    gun_data = None

    for file_path in file_list:
        if file_path.endswith('es0.db'):
            es0_database = file_path
            tables = __init__.get_sqlite_table_names(file_path)

            if 'all_photos' in tables:
                try:
                    photos_data = __init__.read_sqlite_table(
                        file_path, 'all_photos',
                        columns='_id, photo_id, image_url, local_file_path, fingerprint, timestamp')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'contact_search' in tables:
                try:
                    contact_search_data = __init__.read_sqlite_table(
                        file_path, 'contact_search',
                        columns='search_person_id, search_key')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'contacts' in tables:
                try:
                    contacts_data = __init__.read_sqlite_table(
                        file_path, 'contacts',
                        columns='person_id, gaia_id, name, last_updated_time, profile_type, '
                                'profile_state, in_my_circles, blocked')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'guns' in tables:
                try:
                    gun_data = __init__.read_sqlite_table(
                        file_path, 'guns',
                        columns='_id, creation_time, collapsed_description, collapsed_destination, '
                                'collapsed_heading, read_state, seen, activity_id, event_id, album_id, '
                                'community_id, updated_version, PHOTOS')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    google_plus_photos_list = []
    google_plus_contacts_list = []
    google_plus_guns_list = []
    google_plus_data = OrderedDict()

    # Add data from es0.db database
    # Add data from all_photos table to google_plus_data
    if photos_data:
        for entry in photos_data:
            google_plus_data['Database'] = es0_database
            google_plus_data['Table'] = 'all_photos'
            google_plus_data['All Photos Id'] = entry[0]
            google_plus_data['Photo Id'] = entry[1]
            google_plus_data['Image Url'] = entry[2]
            google_plus_data['Local File Path'] = entry[3]
            google_plus_data['Fingerprint'] = entry[4]
            try:
                google_plus_data['Timestamp'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(int(entry[5]) / 1000.))
            except TypeError:
                google_plus_data['Timestamp'] = ''

            google_plus_photos_list.append(google_plus_data)
            google_plus_data = OrderedDict()

    # Add data from contact_search table to google_plus_data
    if contact_search_data:
        for entry in contact_search_data:
            google_plus_data['Database'] = es0_database
            google_plus_data['Table'] = 'contact_search'
            google_plus_data['Search Id'] = entry[0]
            google_plus_data['Person Id'] = ''
            google_plus_data['Gaia Id'] = ''
            google_plus_data['Search Key'] = entry[1]
            google_plus_data['Name'] = ''
            google_plus_data['Profile Type'] = ''
            google_plus_data['Profile State'] = ''
            google_plus_data['In My Circles'] = ''
            google_plus_data['Blocked'] = ''
            google_plus_data['Last Updated'] = ''

            google_plus_contacts_list.append(google_plus_data)
            google_plus_data = OrderedDict()

    # Add data from contacts table to google_plus_data
    if contacts_data:
        for entry in contacts_data:
            google_plus_data['Database'] = es0_database
            google_plus_data['Table'] = 'contacts'
            google_plus_data['Search Id'] = ''
            google_plus_data['Person Id'] = entry[0]
            google_plus_data['Gaia Id'] = entry[1]
            google_plus_data['Search Key'] = ''
            google_plus_data['Name'] = entry[2]
            google_plus_data['Profile Type'] = entry[4]
            google_plus_data['Profile State'] = entry[5]
            google_plus_data['In My Circles'] = entry[6]
            google_plus_data['Blocked'] = entry[7]
            try:
                google_plus_data['Last Updated'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(int(entry[3]) / 1000.))
            except TypeError:
                google_plus_data['Last Updated'] = ''

            google_plus_contacts_list.append(google_plus_data)
            google_plus_data = OrderedDict()

    # Add data from gun table to google_plus_data
    if gun_data:
        for entry in gun_data:
            google_plus_data['Database'] = es0_database
            google_plus_data['Table'] = 'guns'
            google_plus_data['Guns Id'] = entry[0]
            google_plus_data['Activity Id'] = entry[7]
            google_plus_data['Album Id'] = entry[9]
            google_plus_data['Community Id'] = entry[10]
            google_plus_data['Event Id'] = entry[8]
            google_plus_data['Collapsed Heading'] = entry[4]
            google_plus_data['Collapsed Description'] = entry[2]
            google_plus_data['Collapsed Destination'] = entry[3]
            try:
                google_plus_data['Creation Time'] = prtime(entry[1])
            except TypeError:
                google_plus_data['Creation Time'] = ''
            try:
                google_plus_data['Updated Version'] = prtime((entry[11]))
            except TypeError:
                google_plus_data['Updated Version'] = ''
            google_plus_data['Read State'] = entry[5]
            google_plus_data['Seen'] = entry[6]
            google_plus_data['Photos'] = entry[12]

            google_plus_guns_list.append(google_plus_data)
            google_plus_data = OrderedDict()

    return google_plus_photos_list, google_plus_contacts_list, google_plus_guns_list


def prtime(timestamp):
    """
    Converts prtime timestamps.

    :param timestamp: A prtime timestamp
    :return: A datetime timestamp in format: Y-m-d H:M:S
    """
    temp = (int(timestamp) / 1000000)
    try:
        dt = datetime.datetime.utcfromtimestamp(temp)
        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        timestamp = ''

    return timestamp