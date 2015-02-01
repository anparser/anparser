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
__date__ = '20150129'
__version__ = '0.00'

from collections import OrderedDict
import logging
import yara
import pandas as pd

path = None
match = None
yara_list = []


def yara_parser(file_list, custom_rule=None):
    """
    Parses files for Malware signatures with Yara

    :param file_list: List of all files
    :return: Dictionary of matches
    """
    if custom_rule:
        rules = yara.compile(source=custom_rule)
    else:
        rules = yara.compile('plugins/other_plugins/signatures/rules.yara')

    for file_path in file_list:
        try:
            match = rules.match(file_path)
        except yara.libyara_wrapper.YaraMatchError as exception:
            logging.error('Yara Match Error: {0:s}'.format(file_path + " > " + str(exception)))
            pass

        if match:
            yara_processor(match, file_path)

    return pd.DataFrame(yara_list)

def yara_processor(match, path):
    """
    Processes Yara Match for Output

    :param match: A single yara match
    :param path: File path for match
    :return:
    """
    yara_data = OrderedDict()
    rule = match['main'][0]['rule']
    matches = match['main'][0]['matches']
    strings = match['main'][0]['strings']
    meta = match['main'][0]['meta']
    tags = match['main'][0]['tags']

    for string in strings:
        yara_data['File Path'] = path
        yara_data['Rule'] = rule
        yara_data['Matches'] = str(matches)
        if meta != {}:
            try:
                yara_data['Author'] = meta['author']
            except KeyError:
                yara_data['Author'] = ''
            try:
                yara_data['Description'] = meta['description']
            except KeyError:
                yara_data['Description'] = ''
        else:
            yara_data['Author'] = ''
            yara_data['Description'] = ''
        yara_data['Flag'] = string['flags']
        yara_data['Identifier'] = string['identifier']
        yara_data['Data'] = string['data']
        yara_data['Offset'] = string['offset']
        if tags == []:
            yara_data['Tags'] = ''
        else:
            yara_data['Tags'] = tags

        yara_list.append(yara_data)
        yara_data = OrderedDict()


