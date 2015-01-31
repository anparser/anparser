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
__date__ = '20150123'
__version__ = '0.00'

import xml_processor
import pandas as pd
from collections import OrderedDict
import time

def google_plus(file_listing):
    """
    Reads and processes xml data from google.android.apps.plus

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    plus_accounts_xml = None
    plus_data = []

    for file_entry in file_listing:
        if file_entry.endswith(u'accounts.xml') and file_entry.count(u'com.google.android.apps.plus') > 0:
            plus_accounts_xml = file_entry
            plus_data = xml_processor.parse_xml_file_notree(file_entry)

    plus_data_list = []
    plus_dict_data = OrderedDict()

    # Add data from XML file to plus_data
    if plus_data:
        plus_dict_data[u'XML File'] = plus_accounts_xml
        for entry in plus_data:
            if entry[u'name'] == u'0.stable_account_id':
                plus_dict_data[u'Account Id'] = entry[u'text_entry']
            elif entry[u'name'] == u'0.account_name':
                plus_dict_data[u'Account Name'] = entry[u'text_entry']
            elif entry[u'name'] == u'0.display_name':
                plus_dict_data[u'Display Name'] = entry[u'text_entry']
            elif entry[u'name'] == u'0.LoginManager.build_version':
                plus_dict_data[u'Build Version'] = entry[u'text_entry']
            elif entry[u'name'] == u'0.last_updated':
                try:
                    plus_dict_data[u'Last Updated'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                    time.gmtime(
                                                                                        int(entry[u'value']) / 1000.))
                except TypeError:
                    plus_dict_data[u'Last Updated'] = ''

        plus_data_list.append(plus_dict_data)
        plus_dict_data = OrderedDict()

    return pd.DataFrame(plus_data_list)