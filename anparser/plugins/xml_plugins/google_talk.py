# -*- coding: utf-8 -*-
__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '20150113'
__version__ = '0.00'

"""
anparser - an Open Source Android Artifact Parser
Copyright (C) 2015  Chapin Bryce

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

import __init__
import collections
import base64
import os


def google_talk(file_listing):
    """
    Parse XML Google Talk list for data about account and circles

    :param file_listing: List of files to process
    :return: List of dictionaries containing XMl entries
    """
    g_talk_xml = None
    g_talk_data_list = []

    for file_entry in file_listing:
        if os.path.basename(file_entry).startswith('account-') and file_entry.endswith('.xml'):
            g_talk_xml = file_entry
            data = __init__.parse_xml_file_notree(file_entry)

            account_name = os.path.basename(file_entry).strip('account-').split('.xml', 1)[0]

            g_talk_data = collections.OrderedDict()
            g_talk_data['XML File'] = g_talk_xml
            g_talk_data['Name'] = 'Account'
            g_talk_data['Text Entry'] = account_name
            g_talk_data['Value'] = ''
            g_talk_data['Circle'] = ''
            g_talk_data_list.append(g_talk_data)
            g_talk_data = collections.OrderedDict()

            for entry in data:
                circle_name = ''
                if entry['Name'].startswith('chat_acl_settings_circle'):
                    try:
                        circle_name = entry['name'].split('==', 1)[1]
                    except:
                        circle_name = ''
                try:
                    g_talk_data['Name'] = entry['name']
                except:
                    g_talk_data['Name'] = ''

                try:
                    g_talk_data['Text Entry'] = entry['text_entry']
                except:
                    g_talk_data['Text Entry'] = ''

                try:
                    g_talk_data['Value'] = entry['value']
                except:
                    g_talk_data['Value'] = ''

                g_talk_data['Circle'] = base64.b64decode(circle_name)

                g_talk_data_list.append(g_talk_data)
                g_talk_data = collections.OrderedDict()

    return g_talk_data_list