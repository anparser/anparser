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
import sqlite_processor


def android_calendar(file_list):
    """
    Parses calendar.db from com.android.providers.calendar

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # Initialize table variables: Attendees, Events, Reminders, Tasks
    attendees_data = None
    events_data = None
    reminders_data = None
    tasks_data = None

    for file_path in file_list:
        if file_path.endswith(u'calendar.db'):
            tables = sqlite_processor.get_sqlite_table_names(file_path)
            if u'Attendees' in tables:
                attendees_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Attendees', [u'_id', u'event_id', u'attendeeName', u'attendeeEmail'])

            if u'Events' in tables:
                events_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Events', [u'_id', u'title', u'eventLocation', u'description',
                                           u'dtstart', u'dtend', u'eventTimezone', u'lastDate',
                                           u'organizer', u'deleted', u'latitude', u'longitude'])

            if u'Reminders' in tables:
                reminders_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Reminders', ['_id', 'event_id', 'minutes'])

            if u'Tasks' in tables:
                tasks_data = sqlite_processor.read_sqlite_table(
                    file_path, u'Tasks', [u'_id', u'clientId', u'utc_due_date', u'recurrence_type',
                                          u'recurrence_start', u'recurrence_until', u'reminder_set',
                                          u'reminder_time', u'subject', u'body', u'deleted'])

    return attendees_data, events_data, reminders_data, tasks_data