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
__date__ = '20150102'
__version__ = '0.00'

import sqlite3


def get_sqlite_table_names(db_path):
    """
    Read all SQLite table names

    :param db_path: String path to database
    :return: List of table names
    """

    # TODO: Add ability to filter responsive table names

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute('Select name from sqlite_master where type = \'table\';')

    # convert tuples to lists

    tmp = cur.fetchall()
    tmp2 = []
    for i in tmp:
        for x in i:
            tmp2.append(x)

    return tmp2


def get_sqlite_veiw_info(db_path):
    """
    Read all SQLite table names
    :param db_path: String path to database
    :return: List of table names
    """

    # TODO: Add ability to filter responsive table names

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute('Select name, sql from sqlite_master where type = \'view\';')

    # convert tuples to lists

    tmp = cur.fetchall()
    tmp2 = []
    for i in tmp:
        tmp2.append(i[0])

    return tmp2


def read_sqlite_table(db_path, table_name, columns=None):
    """
    Read data from a single table in SQLite3

    :param db_path: string full path to database
    :param table_name: string name of table within database
    :param columns: string of table names to parse
    :return: List of all entries
    """

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    if columns:
        cur.execute('select ' + columns + ' from ' + table_name + ';', )
    else:
        cur.execute('select * from ' + table_name + ';', )

    return cur.fetchall()


def read_sqlite_tables(db_path):
    """
    Scans for available tables and reads the data within them

    :param db_path: String path to database
    :return: Dictionary with keys for table names and values for the data within the table
    """

    table_dict = dict()

    for table_name in get_sqlite_table_names(db_path):
        table_dict[table_name] = read_sqlite_table(db_path, table_name)

    return table_dict