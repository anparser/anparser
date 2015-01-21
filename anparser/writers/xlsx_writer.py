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
__date__ = '20150117'
__version__ = '0.00'

import pandas as pd
import logging

#TODO: Add try & except

def xlsx_writer(data, file_name):
    """
    Write list of dictionaries of data to a file

    :param data: list of dictionaries
    :param file_name: file name to write to
    :return: Completion State
    """

    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    for key in data.keys():
        data[key].to_excel(writer, '{0:s}'.format(key), index=False)
    writer.close()