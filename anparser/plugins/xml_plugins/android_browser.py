# -*- coding: utf-8 -*-

__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '20150112'
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


def android_browser(file_listing):
    """
    reads user default and preferences from XMl files
    :param file_listing: list of file paths
    :return: list of dictionaries for user_defaults and preferences
    """

    user_defaults = []
    browser_prefs = []

    for file_path in file_listing:
        if file_path.endswith('omadm_node.xml'):
            user_defaults = __init__.parse_xml_file_notree(file_path)
        elif file_path.endswith('com.android.browser_preferences.xml'):
            browser_prefs = __init__.parse_xml_file_notree(file_path)

    return user_defaults, browser_prefs