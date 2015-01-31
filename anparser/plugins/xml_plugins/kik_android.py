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
__date__ = '20150119'
__version__ = '0.00'

import xml_processor
import pandas as pd
from collections import OrderedDict
import time

def kik_android(file_listing):
    """
    Reads and processes xml data from kik_android

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    kik_pref_xml = None
    kik_per_xml = None
    kik_data = []
    kik_persistance_data = []

    for file_entry in file_listing:
        if file_entry.endswith(u'KikPreferences.xml'):
            kik_pref_xml = file_entry
            kik_data = xml_processor.parse_xml_file_notree(file_entry)
        if file_entry.endswith(u'KikUltraPersistence.xml'):
            kik_per_xml = file_entry
            kik_persistance_data = xml_processor.parse_xml_file_notree(file_entry)

    kik_data_list = []
    kik_dict_data = OrderedDict()

    # Add data from XML file to kik_data
    if kik_data:
        kik_dict_data[u'XML Files'] = kik_pref_xml + u' & ' + kik_per_xml
        for entry in kik_data:
            if entry[u'name'] == u'kik.version_number':
                kik_dict_data[u'Kik Version'] = entry[u'text_entry']
            if entry[u'name'] == u'CredentialData.jid':
                kik_dict_data[u'Jid'] = entry[u'text_entry']
            elif entry[u'name'] == u'user_profile_firstName':
                kik_dict_data[u'First Name'] = entry[u'text_entry']
            elif entry[u'name'] == u'user_profile_lastName':
                kik_dict_data[u'Last Name'] = entry[u'text_entry']
            elif entry[u'name'] == u'user_profile_email':
                kik_dict_data[u'Email'] = entry[u'text_entry']
            elif entry[u'name'] == u'user_profile_username':
                kik_dict_data[u'Username'] = entry[u'text_entry']
            elif entry[u'name'] == u'kik.registrationtime':
                try:
                    kik_dict_data[u'Registration Time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                       time.gmtime(
                                                                           int(entry[u'value']) / 1000.))
                except TypeError:
                    kik_dict_data[u'Registration Time'] = u''

    if kik_persistance_data:
        for entry in kik_persistance_data:
            if entry[u'name'] == u'kik.deviceid':
                kik_dict_data[u'Device Id'] = entry[u'text_entry']
            elif entry[u'name'] == u'kik.has-kik-ever-run':
                kik_dict_data[u'Has Kik Ever Run'] = entry[u'value']

        kik_data_list.append(kik_dict_data)
        kik_dict_data = OrderedDict()

    return pd.DataFrame(kik_data_list)