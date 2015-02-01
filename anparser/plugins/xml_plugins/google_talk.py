# -*- coding: utf-8 -*-
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

__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '20150113'
__version__ = '0.00'

import collections
import base64
import os

import pandas as pd

from processors import xml_processor


def google_talk(file_listing):
    """
    Parse XML Google Talk list for data about account and circles

    :param file_listing: List of files to process
    :return: List of dictionaries containing XMl entries
    """
    g_talk_xml = None
    g_talk_data_list = []

    for file_entry in file_listing:
        if os.path.basename(file_entry).startswith(u'account-') and file_entry.endswith(u'.xml'):
            g_talk_xml = file_entry
            data = xml_processor.parse_xml_file_notree(file_entry)

            account_name = os.path.basename(file_entry).strip(u'account-').split(u'.xml', 1)[0]

            g_talk_data = collections.OrderedDict()
            g_talk_data[u'XML File'] = g_talk_xml
            g_talk_data[u'Name'] = u'Account'
            g_talk_data[u'Text Entry'] = account_name
            g_talk_data[u'Value'] = u''
            g_talk_data[u'Circle'] = u''
            g_talk_data_list.append(g_talk_data)
            g_talk_data = collections.OrderedDict()

            for entry in data:
                circle_name = u''
                if entry[u'Name'].startswith(u'chat_acl_settings_circle'):
                    try:
                        circle_name = entry[u'name'].split('==', 1)[1]
                    except:
                        circle_name = u''
                try:
                    g_talk_data[u'Name'] = entry[u'name']
                except:
                    g_talk_data[u'Name'] = u''

                try:
                    g_talk_data[u'Text Entry'] = entry[u'text_entry']
                except:
                    g_talk_data[u'Text Entry'] = u''

                try:
                    g_talk_data[u'Value'] = entry[u'value']
                except:
                    g_talk_data[u'Value'] = u''

                g_talk_data[u'Circle'] = base64.b64decode(circle_name)

                g_talk_data_list.append(g_talk_data)
                g_talk_data = collections.OrderedDict()

    return pd.DataFrame(g_talk_data_list)