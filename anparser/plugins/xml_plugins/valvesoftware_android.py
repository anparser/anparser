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
__date__ = '20150124'
__version__ = '0.00'

from collections import OrderedDict

import pandas as pd

from ingest import xml_processor


def valvesoftware_android(file_listing):
    """
    Reads and processes xml data from valvesoftware_android

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    valve_pref_xml = None
    valve_data = []

    for file_entry in file_listing:
        if file_entry.endswith(u'steamumqcommunication.xml'):
            valve_pref_xml = file_entry
            valve_data = xml_processor.parse_xml_file_notree(file_entry)

    valve_data_list = []
    valve_dict_data = OrderedDict()

    # Add data from XML file to valve_data
    if valve_data:
        valve_dict_data[u'XML File'] = valve_pref_xml
        for entry in valve_data:
            if entry[u'name'] == u'umqid':
                valve_dict_data[u'Umq Id'] = entry[u'text_entry']


        valve_data_list.append(valve_dict_data)
        valve_dict_data = OrderedDict()

    return pd.DataFrame(valve_data_list)