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
__date__ = '20150115'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import time


def android_calendar(file_list):
    """
    Parses calendar.db from com.android.providers.calendar

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # Initialize table variables: Attendees, Events, Reminders, Tasks
    calendar_database = None
    attendees_data = None
    events_data = None
    reminders_data = None
    tasks_data = None

    for file_path in file_list:
        if file_path.endswith('calendar.db'):
            calendar_database = file_path
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []
            if 'Attendees' in tables:
                try:
                    attendees_data = __init__.read_sqlite_table(
                        file_path, 'Attendees',
                        columns='_id, event_id, attendeeName, attendeeEmail')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'Events' in tables:
                try:
                    events_data = __init__.read_sqlite_table(
                        file_path, 'Events',
                        columns='_id, title, eventLocation, description, dtstart, dtend, '
                                'eventTimezone, lastDate, organizer, deleted, latitude, '
                                'longitude')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'Reminders' in tables:
                try:
                    reminders_data = __init__.read_sqlite_table(
                        file_path, 'Reminders',
                        columns='_id, event_id, minutes')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass
            if 'Tasks' in tables:
                try:
                    tasks_data = __init__.read_sqlite_table(
                        file_path, 'Tasks',
                        columns='_id, clientId, utc_due_date, recurrence_type, '
                                'recurrence_start, recurrence_until, reminder_set, '
                                'reminder_time, subject, body, deleted')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    calendar_data_list = []
    calendar_data = OrderedDict()

    # Add data from calendar.db to calendar_data_list
    # Add data from Attendees table to calendar_data
    if attendees_data:
        for entry in attendees_data:
            calendar_data['Database'] = calendar_database
            calendar_data['Table'] = 'Attendees'
            calendar_data['Attendee Id'] = entry[0]
            calendar_data['Event Id'] = entry[1]
            calendar_data['Reminder Id'] = ''
            calendar_data['Task Id'] = ''
            calendar_data['Client Id'] = ''
            calendar_data['Attendee Name'] = entry[2]
            calendar_data['Attendee Email'] = entry[3]
            calendar_data['Reminder Set'] = ''
            calendar_data['Reminder Time'] = ''
            calendar_data['Reminder (Minutes)'] = ''
            calendar_data['Organizer'] = ''
            calendar_data['Title'] = ''
            calendar_data['Description'] = ''
            calendar_data['Deleted'] = ''
            calendar_data['Event Start'] = ''
            calendar_data['Event End'] = ''
            calendar_data['Event Timezone'] = ''
            calendar_data['Last Date'] = ''
            calendar_data['UTC Due Date'] = ''
            calendar_data['Recurrence Type'] = ''
            calendar_data['Recurrence Start'] = ''
            calendar_data['Recurrence Until'] = ''
            calendar_data['Event Location'] = ''
            calendar_data['Latitude'] = ''
            calendar_data['Longitude'] = ''

            calendar_data_list.append(calendar_data)
            calendar_data = OrderedDict()

    # Add data from Reminders table to calendar_data
    if reminders_data:
        for entry in reminders_data:
            calendar_data['Database'] = calendar_database
            calendar_data['Table'] = 'Reminders'
            calendar_data['Attendee Id'] = ''
            calendar_data['Event Id'] = entry[1]
            calendar_data['Reminder Id'] = entry[0]
            calendar_data['Task Id'] = ''
            calendar_data['Client Id'] = ''
            calendar_data['Attendee Name'] = ''
            calendar_data['Attendee Email'] = ''
            calendar_data['Reminder Set'] = ''
            calendar_data['Reminder Time'] = ''
            calendar_data['Reminder (Minutes)'] = entry[2]
            calendar_data['Organizer'] = ''
            calendar_data['Title'] = ''
            calendar_data['Description'] = ''
            calendar_data['Deleted'] = ''
            calendar_data['Event Start'] = ''
            calendar_data['Event End'] = ''
            calendar_data['Event Timezone'] = ''
            calendar_data['Last Date'] = ''
            calendar_data['UTC Due Date'] = ''
            calendar_data['Recurrence Type'] = ''
            calendar_data['Recurrence Start'] = ''
            calendar_data['Recurrence Until'] = ''
            calendar_data['Event Location'] = ''
            calendar_data['Latitude'] = ''
            calendar_data['Longitude'] = ''

            calendar_data_list.append(calendar_data)
            calendar_data = OrderedDict()

    # Add data from Events table to calendar_data
    if events_data:
        for entry in events_data:
            calendar_data['Database'] = calendar_database
            calendar_data['Table'] = 'Events'
            calendar_data['Attendee Id'] = ''
            calendar_data['Event Id'] = entry[0]
            calendar_data['Reminder Id'] = ''
            calendar_data['Task Id'] = ''
            calendar_data['Client Id'] = ''
            calendar_data['Attendee Name'] = ''
            calendar_data['Attendee Email'] = ''
            calendar_data['Reminder Set'] = ''
            calendar_data['Reminder Time'] = ''
            calendar_data['Reminder (Minutes)'] = ''
            calendar_data['Organizer'] = entry[8]
            calendar_data['Title'] = entry[1]
            calendar_data['Description'] = entry[3]
            calendar_data['Deleted'] = entry[9]
            try:
                calendar_data['Event Start'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[4] / 1000.))
            except TypeError:
                calendar_data['Event Start'] = ''
            try:
                calendar_data['Event End'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[5] / 1000.))
            except TypeError:
                calendar_data['Event End'] = ''
            calendar_data['Event Timezone'] = entry[6]
            try:
                calendar_data['Last Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[7] / 1000.))
            except TypeError:
                calendar_data['Last Date'] = ''
            calendar_data['UTC Due Date'] = ''
            calendar_data['Recurrence Type'] = ''
            calendar_data['Recurrence Start'] = ''
            calendar_data['Recurrence Until'] = ''
            calendar_data['Event Location'] = entry[2]
            calendar_data['Latitude'] = entry[10]
            calendar_data['Longitude'] = entry[11]

            calendar_data_list.append(calendar_data)
            calendar_data = OrderedDict()

    # Add data from Tasks table to calendar_data
    if tasks_data:
        for entry in tasks_data:
            calendar_data['Database'] = calendar_database
            calendar_data['Table'] = 'Tasks'
            calendar_data['Attendee Id'] = ''
            calendar_data['Event Id'] = ''
            calendar_data['Reminder Id'] = ''
            calendar_data['Task Id'] = entry[0]
            calendar_data['Client Id'] = entry[1]
            calendar_data['Attendee Name'] = ''
            calendar_data['Attendee Email'] = ''
            calendar_data['Reminder Set'] = entry[6]
            try:
                calendar_data['Reminder Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[7] / 1000.))
            except TypeError:
                calendar_data['Reminder Time'] = ''
            calendar_data['Reminder (Minutes)'] = entry[2]
            calendar_data['Organizer'] = ''
            calendar_data['Title'] = entry[8]
            calendar_data['Description'] = entry[9]
            calendar_data['Deleted'] = entry[10]
            calendar_data['Event Start'] = ''
            calendar_data['Event End'] = ''
            calendar_data['Event Timezone'] = ''
            calendar_data['Last Date'] = ''
            try:
                calendar_data['UTC Due Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.))
            except TypeError:
                calendar_data['UTC Due Date'] = ''
            calendar_data['Recurrence Type'] = entry[3]
            calendar_data['Recurrence Start'] = entry[4]
            calendar_data['Recurrence Until'] = entry[5]
            calendar_data['Event Location'] = ''
            calendar_data['Latitude'] = ''
            calendar_data['Longitude'] = ''

            calendar_data_list.append(calendar_data)
            calendar_data = OrderedDict()

    return calendar_data_list