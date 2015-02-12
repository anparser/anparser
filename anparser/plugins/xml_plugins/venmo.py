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
__date__ = '20150212'
__version__ = '0.00'

from collections import OrderedDict
import time

import pandas as pd

from ingest import xml_processor


def venmo(file_listing):
    """
    Reads and processes xml data from Venmo.xml

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    venmo_pref_xml = None
    venmo_data = []

    for file_entry in file_listing:
        if file_entry.endswith(u'Venmo.xml'):
            venmo_pref_xml = file_entry
            venmo_data = xml_processor.parse_xml_file_notree(file_entry)

    venmo_data_list = []
    venmo_dict_data = OrderedDict()

    # Add data from XML file to valve_data
    if venmo_data:
        venmo_dict_data[u'XML File'] = venmo_pref_xml
        for entry in venmo_data:
            if entry[u'name'] == u'username':
                venmo_dict_data[u'Username'] = entry[u'text_entry']
            if entry[u'name'] == u'userId':
                venmo_dict_data[u'User Id'] = entry[u'value']
            if entry[u'name'] == u'num_friends':
                venmo_dict_data[u'Number Friends'] = entry[u'value']
            if entry[u'name'] == u'last_venmofriends_update':
                venmo_dict_data[u'Last Venmo Friends Update'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                              time.gmtime(int(entry[u'value']) / 1000.))
            if entry[u'name'] == u'facebook_auto_friend_allowed':
                venmo_dict_data[u'Facebook Auto-Add On'] = entry[u'value']
            if entry[u'name'] == u'funding_type':
                venmo_dict_data[u'Funding Type'] = entry[u'text_entry']
            if entry[u'name'] == u'this_device_id':
                venmo_dict_data[u'Device Id'] = entry[u'text_entry']
            if entry[u'name'] == u'user_balance':
                venmo_dict_data[u'User Balance'] = entry[u'value']
            if entry[u'name'] == u'default_audience':
                venmo_dict_data[u'Default Audience'] = entry[u'text_entry']
            if entry[u'name'] == u'user_email':
                venmo_dict_data[u'User Email'] = entry[u'text_entry']
            if entry[u'name'] == u'num_notifs':
                venmo_dict_data['Number Notifications'] = entry[u'value']
            if entry[u'name'] == u'app_version_login':
                venmo_dict_data['App Version'] = entry[u'value']
            if entry[u'name'] == u'num_facebook_friends_on_venmo':
                venmo_dict_data['Number Facebook Friends on Venmo'] = entry[u'value']
            if entry[u'name'] == u'contact_auto_friend_allowed':
                venmo_dict_data['Contact Auto-Add On'] = entry[u'value']
            if entry[u'name'] == u'full_name':
                venmo_dict_data['Full Name'] = entry[u'text_entry']


        venmo_data_list.append(venmo_dict_data)
        venmo_dict_data = OrderedDict()

    return pd.DataFrame(venmo_data_list)