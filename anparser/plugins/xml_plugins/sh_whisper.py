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
__date__ = '20150213'
__version__ = '0.00'

from collections import OrderedDict
import time

import pandas as pd

from ingest import xml_processor


def sh_whisper(file_listing):
    """
    Reads and processes xml data from sh_whisper

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    pref_xml = None
    apprate_xml = None
    whisper_data = []
    apprate_data = []

    for file_entry in file_listing:
        if file_entry.endswith(u'apprate_prefs.xml') and file_entry.count('sh.whisper') > 0:
            apprate_xml = file_entry
            apprate_data = xml_processor.parse_xml_file_notree(file_entry)
        if file_entry.endswith(u'sh.whisper_preferences.xml'):
            pref_xml = file_entry
            whisper_data = xml_processor.parse_xml_file_notree(file_entry)

    whisper_data_list = []
    whisper_dict_data = OrderedDict()

    # Add data from XML file to kik_data
    if apprate_data:
        whisper_dict_data[u'XML Files'] = pref_xml + u' & ' + apprate_xml
        for entry in apprate_data:
            if entry[u'name'] == u'launch_count':
                whisper_dict_data[u'Launch Count'] = entry[u'value']
            elif entry[u'name'] == u'date_firstlaunch':
                try:
                    whisper_dict_data[u'First Launch'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                       time.gmtime(int(entry[u'value']) / 1000.))
                except TypeError:
                    whisper_dict_data[u'First Launch'] = u''

    if whisper_data:
        for entry in whisper_data:
            if entry[u'name'] == u'uid':
                whisper_dict_data[u'User Id'] = entry[u'text_entry']
            elif entry[u'name'] == u'hearts':
                whisper_dict_data[u'Hearts (Likes) Count'] = entry[u'value']
            elif entry[u'name'] == u'creates':
                whisper_dict_data[u'Whisper Count'] = entry[u'value']
            elif entry[u'name'] == u'logins':
                whisper_dict_data[u'Login Count'] = entry[u'value']
            elif entry[u'name'] == u'lattitude_prefs_key':
                whisper_dict_data[u'Latitude'] = entry[u'value']
            elif entry[u'name'] == u'longitude_prefs_key':
                whisper_dict_data[u'Longitude'] = entry[u'value']
            elif entry[u'name'] == u'fbid':
                whisper_dict_data[u'fbid'] = entry[u'text_entry']
            elif entry[u'name'] == u'puid':
                whisper_dict_data[u'puid'] = entry[u'text_entry']
            elif entry[u'name'] == u'last_time_in_app':
                try:
                    whisper_dict_data[u'Last Time In App'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                       time.gmtime(int(entry[u'value']) / 1000.))
                except IndexError:
                    whisper_dict_data[u'Last Time In App'] = u''
            elif entry[u'name'] == u'nickname':
                whisper_dict_data[u'Nickname'] = entry[u'text_entry']
            elif entry[u'name'] == u'wgcm_appVersion':
                whisper_dict_data[u'App Version'] = entry[u'value']
            elif entry[u'name'] == u'replies':
                whisper_dict_data[u'Reply Count'] = entry[u'value']

        whisper_data_list.append(whisper_dict_data)
        whisper_dict_data = OrderedDict()

    return pd.DataFrame(whisper_data_list)