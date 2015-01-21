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

import __init__
from collections import OrderedDict
import time

def snapchat_android(file_listing):
    """
    Reads and processes xml data from snapchat_android

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    snapchat_data = []

    for file_entry in file_listing:
        if file_entry.endswith('com.snapchat.android_preferences.xml'):
            snapchat_data = __init__.parse_xml_file_notree(file_entry)

    snapchat_data_list = []
    snapchat_dict_data = OrderedDict()

    # Add data from XML file to snapchat_data
    if snapchat_data:
        for entry in snapchat_data:
            if entry['name'] == 'device_id':
                snapchat_dict_data['Device ID'] = entry['text_entry']
            elif entry['name'] == 'phone_number':
                snapchat_dict_data['Phone Number'] = entry['text_entry']
            elif entry['name'] == 'lastSuccessfulLoginUsername':
                snapchat_dict_data['Last Successful Login Username'] = entry['text_entry']
            elif entry['name'] == 'username':
                snapchat_dict_data['Username'] = entry['text_entry']
            elif entry['name'] == 'email':
                snapchat_dict_data['Email'] = entry['text_entry']
            elif entry['name'] == 'num_snaps_sent':
                snapchat_dict_data['Snaps Sent'] = entry['value']
            elif entry['name'] == 'num_snaps_received':
                snapchat_dict_data['Snaps Received'] = entry['value']
            elif entry['name'] == 'has_pending_notifications':
                snapchat_dict_data['Pending Notifications'] = entry['value']
            elif entry['name'] == 'num_best_friends':
                snapchat_dict_data['Number Best Friends'] = entry['value']
            elif entry['name'] == 'last_external_image_taken_timestamp':
                try:
                    snapchat_dict_data['Last External Image Taken'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                    time.gmtime(
                                                                                        int(entry['value']) / 1000.))
                except TypeError:
                    snapchat_dict_data['Last External Image Taken'] = ''
            elif entry['name'] == 'last_seen_added_me_timestamp':
                try:
                    snapchat_dict_data['Last Seen Added Me Timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                       time.gmtime(
                                                                                           int(entry['value']) / 1000.))
                except TypeError:
                    snapchat_dict_data['Last External Image Taken'] = ''

        snapchat_data_list.append(snapchat_dict_data)
        snapchat_dict_data = OrderedDict()

    return snapchat_data_list