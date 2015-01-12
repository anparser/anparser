__author__ = 'cbryce'
__license__ = ''
__date__ = ''
__version__ = ''

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


def android_vending(file_listing):
    """
    Reads and processes xml data from android_vending

    :param file_listing: list of files
    :return: list of dictionaries containing XML values
    """
    for file_entry in file_listing:
        if file_entry.endswith('finsky.xml') and file_entry.count('com.android.vending') > 0:
            vending_data = __init__.parse_xml_file_notree(file_entry)

    # add all columns to first entry for CSV Writing
    vending_data[0]['value'] = ''
    vending_data[0] = vending_data[0]

    return vending_data
