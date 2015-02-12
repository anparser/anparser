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

import pandas as pd

from ingest import xml_processor


def infraware_office(file_listing):
    """
    Reads and processes xml data from pouserinfo_pref.xml

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    polaris_pref_xml = None
    polaris_data = []

    for file_entry in file_listing:
        if file_entry.endswith(u'pouserinfo_pref.xml'):
            polaris_pref_xml = file_entry
            polaris_data = xml_processor.parse_xml_file_notree(file_entry)

    polaris_data_list = []
    polaris_dict_data = OrderedDict()

    # Add data from XML file to valve_data
    if polaris_data:
        polaris_dict_data[u'XML File'] = polaris_pref_xml
        for entry in polaris_data:
            if entry[u'name'] == u'pouserinfo_has_password':
                polaris_dict_data[u'Has Password'] = entry[u'value']
            if entry[u'name'] == u'pouserinfo_first_name_pref':
                polaris_dict_data[u'First Name'] = entry[u'text_entry']
            if entry[u'name'] == u'pouserinfo_last_name_pref':
                polaris_dict_data[u'Last Name'] = entry[u'text_entry']
            if entry[u'name'] == u'pouserinfo_full_name_pref':
                polaris_dict_data[u'Full Name'] = entry[u'text_entry']
            if entry[u'name'] == u'pouserinfo_user_id':
                polaris_dict_data[u'User Id'] = entry[u'text_entry']


        polaris_data_list.append(polaris_dict_data)
        polaris_dict_data = OrderedDict()

    return pd.DataFrame(polaris_data_list)