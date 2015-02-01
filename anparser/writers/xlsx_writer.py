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
__date__ = '20150131'
__version__ = '0.00'

import pandas as pd
import os
import logging

def xlsx_writer(data_dict, folder_name, xlsx_name):
    """
    Write pandas DataFrame objects to XLSX

    :param data: pandas DataFrame
    :param file_name: file name to write to
    :return: Nothing
    """
    if not os.path.exists(folder_name):
        os.mkdir(folder_name, 0777)
    with pd.ExcelWriter((folder_name + '//' + xlsx_name)) as writer:
        for df in data_dict.keys():
            try:
                data_dict[df].to_excel(writer, sheet_name=df, encoding='utf-8')
            except AttributeError as exception:
                pass