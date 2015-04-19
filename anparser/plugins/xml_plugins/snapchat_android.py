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
__date__ = '20150116'
__version__ = '0.00'

from collections import OrderedDict
import time

import pandas as pd

from ingest import xml_processor


def snapchat_android(file_listing):
    """
    Reads and processes xml data from snapchat_android

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    snapchat_pref_xml = None
    snapchat_data = []

    for file_entry in file_listing:
        if file_entry.endswith(u'com.snapchat.android_preferences.xml'):
            snapchat_pref_xml = file_entry
            snapchat_data = xml_processor.parse_xml_file_notree(file_entry)

    snapchat_data_list = []
    snapchat_dict_data = OrderedDict()

    # Add data from XML file to snapchat_data
    if snapchat_data:
        snapchat_dict_data[u'XML File'] = snapchat_pref_xml
        for entry in snapchat_data:
            if entry[u'name'] == u'device_id':
                snapchat_dict_data[u'Device Id'] = entry[u'text_entry']
            elif entry[u'name'] == u'phone_number':
                snapchat_dict_data[u'Phone Number'] = entry[u'text_entry']
            elif entry[u'name'] == u'lastSuccessfulLoginUsername':
                snapchat_dict_data[u'Last Successful Login Username'] = entry[u'text_entry']
            elif entry[u'name'] == u'username':
                snapchat_dict_data[u'Username'] = entry[u'text_entry']
            elif entry[u'name'] == u'email':
                snapchat_dict_data[u'Email'] = entry[u'text_entry']
            elif entry[u'name'] == u'num_snaps_sent':
                snapchat_dict_data[u'Snaps Sent'] = entry[u'value']
            elif entry[u'name'] == u'num_snaps_received':
                snapchat_dict_data[u'Snaps Received'] = entry[u'value']
            elif entry[u'name'] == u'has_pending_notifications':
                snapchat_dict_data[u'Pending Notifications'] = entry[u'value']
            elif entry[u'name'] == u'num_best_friends':
                snapchat_dict_data[u'Number Best Friends'] = entry[u'value']
            elif entry[u'name'] == u'last_external_image_taken_timestamp':
                try:
                    snapchat_dict_data[u'Last External Image Taken'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                    time.gmtime(
                                                                                        int(entry[u'value']) / 1000.))
                except TypeError:
                    snapchat_dict_data[u'Last External Image Taken'] = u''
            elif entry[u'name'] == u'last_seen_added_me_timestamp':
                try:
                    snapchat_dict_data[u'Last Seen Added Me Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                       time.gmtime(
                                                                                           int(entry[u'value']) / 1000.))
                except TypeError:
                    snapchat_dict_data[u'Last External Image Taken'] = u''

        snapchat_data_list.append(snapchat_dict_data)
        snapchat_dict_data = OrderedDict()

    return pd.DataFrame(snapchat_data_list)