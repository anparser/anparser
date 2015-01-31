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


import xml.etree.ElementTree as ET
from collections import OrderedDict

def parse_xml_file_notree(FILE):
    """
    :param FILE: string path to file
    :return: List of dictionaries
    """

    context = ET.iterparse(FILE, events=['start'])
    context = iter(context)
    event, root = context.next()

    # Setup Variables
    elem_array = []
    ordered_array = OrderedDict()

    for event, elem in context:
        ordered_array = elem.attrib
        ordered_array['text_entry'] = str(elem.text).strip()

        elem_array.append(ordered_array)
        ordered_array = OrderedDict()

    return elem_array