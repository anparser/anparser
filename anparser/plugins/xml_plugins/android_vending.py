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

import pandas as pd

from ingest import xml_processor


def android_vending(file_listing):
    """
    Reads and processes xml data from android_vending

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    vending_data = []
    for file_entry in file_listing:
        if file_entry.endswith(u'finsky.xml') and file_entry.count(u'com.android.vending') > 0:
            vending_data = xml_processor.parse_xml_file_notree(file_entry)

    # add all columns to first entry for CSV Writing
    try:
        vending_data[0][u'value'] = ''
        vending_data[0] = vending_data[0]
    except IndexError:
        pass

    return pd.DataFrame(vending_data)