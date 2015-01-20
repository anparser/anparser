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

import __init__
from collections import OrderedDict
import time

def kik_android(file_listing):
    """
    Reads and processes xml data from kik_android

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    kik_data = []
    kik_persistance_data = []

    for file_entry in file_listing:
        if file_entry.endswith('KikPreferences.xml'):
            kik_data = __init__.parse_xml_file_notree(file_entry)
        if file_entry.endswith('KikUltraPersistence.xml'):
            kik_persistance_data = __init__.parse_xml_file_notree(file_entry)

    kik_data_list = []
    kik_dict_data = OrderedDict()

    # Add data from XML file to kik_data
    if kik_data:
        for entry in kik_data:
            if entry['name'] == 'kik.version_number':
                kik_dict_data['Kik Version'] = entry['text_entry']
            if entry['name'] == 'CredentialData.jid':
                kik_dict_data['Jid'] = entry['text_entry']
            elif entry['name'] == 'user_profile_firstName':
                kik_dict_data['First Name'] = entry['text_entry']
            elif entry['name'] == 'user_profile_lastName':
                kik_dict_data['Last Name'] = entry['text_entry']
            elif entry['name'] == 'user_profile_email':
                kik_dict_data['Email'] = entry['text_entry']
            elif entry['name'] == 'user_profile_username':
                kik_dict_data['Username'] = entry['text_entry']
            elif entry['name'] == 'kik.registrationtime':
                try:
                    kik_dict_data['Registration Time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                       time.gmtime(
                                                                           int(entry['value']) / 1000.))
                except TypeError:
                    kik_dict_data['Registration Time'] = ''

    if kik_persistance_data:
        for entry in kik_persistance_data:
            if entry['name'] == 'kik.deviceid':
                kik_dict_data['Device Id'] = entry['text_entry']
            elif entry['name'] == 'kik.has-kik-ever-run':
                kik_dict_data['Has Kik Ever Run'] = entry['value']

        kik_data_list.append(kik_dict_data)
        kik_dict_data = OrderedDict()

    return kik_data_list