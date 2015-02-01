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

from ingest import sqlite_processor  # , time_processor


def google_plus(file_list):
    """
    Parses database folder from com.google.android.apps.plus

    :param file_list: List of all files
    :return: Dictionary of parsed data from DocList.db
    """
    # Initialize table variables: all_photos, contact_search, contacts, guns,
    photos_data = None
    contact_search_data = None
    contacts_data = None
    gun_data = None

    for file_path in file_list:
        if file_path.endswith(u'es0.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'all_photos' in tables:
                photos_data = sqlite_processor.read_sqlite_table(
                    file_path, u'all_photos',
                    u'_id, photo_id, image_url, local_file_path, fingerprint, timestamp')
                if photos_data is not None:
                    photos_data.timestamp = time_processor.unix_time(photos_data.timestamp)

            if u'contact_search' in tables:
                contact_search_data = sqlite_processor.read_sqlite_table(
                    file_path, u'contact_search',
                    u'search_person_id, search_key')

            if u'contacts' in tables:
                contacts_data = sqlite_processor.read_sqlite_table(
                    file_path, u'contacts',
                    u'person_id, gaia_id, name, last_updated_time, profile_type, '
                    u'profile_state, in_my_circles, blocked')
                if contacts_data is not None:
                    contacts_data.last_updated_time = time_processor.unix_time(contacts_data.last_updated_time)

            if u'guns' in tables:
                gun_data = sqlite_processor.read_sqlite_table(
                    file_path, u'guns',
                    u'_id, creation_time, collapsed_description, collapsed_destination, '
                    u'collapsed_heading, read_state, seen, activity_id, event_id, album_id, '
                    u'community_id, updated_version, PHOTOS')
                if gun_data is not None:
                    gun_data.creation_time = time_processor.prt_time(gun_data.creation_time)
                    gun_data.updated_version = time_processor.prt_time(gun_data.updated_version)

    return photos_data, contact_search_data, contacts_data, gun_data