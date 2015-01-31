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
__date__ = '20140109'
__version__ = '0.00'

import xml_processor
import pandas as pd
import os
import collections


def android_gmail_process(file_to_process):
    """
    Process Gmail.xml file and extract the active account address

    :param file_to_process: string path to a file to process
    :return: list of dictionary to process
    """

    xml_entries_notree = xml_processor.parse_xml_file_notree(file_to_process)

    gmail_dict = collections.OrderedDict()
    gmail_dict_list = []

    if xml_entries_notree:
        for entry in xml_entries_notree:
            gmail_dict[u'XML'] = file_to_process
            for item in entry.keys():
                if item.__contains__(u'name') and entry[u'name'] == u'active-account':
                    gmail_dict[u'Active Account'] = entry[u'text_entry']
                elif item.__contains__(u'name') and entry[u'name'] == u'cache-google-accounts-synced':
                    gmail_dict[u'Cached Google Accounts Synced'] = entry[u'text_entry']
        gmail_dict_list.append(gmail_dict)
        gmail_dict = collections.OrderedDict()

    return pd.DataFrame(gmail_dict_list)


def android_gmail(fileListing):
    """
    Parse file list to search for relevant files
    :param fileListing: List of files to search
    :return: data from parser
    """

    for file_path in fileListing:
        if file_path.endswith(u'Gmail.xml'):
            return android_gmail_process(file_path)

    return None