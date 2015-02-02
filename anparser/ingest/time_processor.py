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

import datetime
import time


def unix_time(dataframe, op=None):
    """
    Converts unix timestamps from a specific pandas DataFrame column.

    :param dataframe: a pandas DataFrame object with a column specification
    :return: A human readable timestamp
    """
    mul = 1000.
    if op is not None:
        mul = 1.
        try:
            return dataframe.apply(
                lambda x: time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.gmtime(x / mul)) if str(x) != 'nan' and x != None and x != 0 else None)
        except TypeError:
            pass


def chrome_time(dataframe):
    """

    :param dataframe:
    :return:
    """
    offset = 11644473600000
    return dataframe.apply(
        lambda x: datetime.datetime.utcfromtimestamp(
            ((x / 1000) - offset) * (1*10**-3)).strftime(
            '%Y-%m-%d %H:%M:%S') if str(x) != 'nan' and x != None and x != 0 else None)

def prt_time(dataframe):
    """

    :param dataframe:
    :return:
    """
    return dataframe.apply(
        lambda x: datetime.datetime.utcfromtimestamp(
            x / 1000000).strftime('%Y-%m-%d %H:%M:%S') if str(x) != 'nan' and x != None and x != 0 else None)