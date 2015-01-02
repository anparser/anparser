__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '20150102'
__version__ = '0.00'

import sqlite_plugins
import time


def android_contacts(file_list):

    # Initialize Variable
    raw_contacts_data = None
    accounts_data = None
    phone_lookup_data = None

    for file_path in file_list:
        if file_path.endswith('contacts2.db'):
            tables = sqlite_plugins.get_sqlite_table_names(file_path)
            if 'raw_contacts' in tables:
                raw_contacts_data = sqlite_plugins.read_sqlite_table(file_path, 'raw_contacts',
                                                                     columns='contact_id, display_name, modified_time')
            if 'accounts' in tables:
                accounts_data = sqlite_plugins.read_sqlite_table(file_path, 'accounts',
                                                                 columns='_id, account_name, account_type')
            if 'phone_lookup' in tables:
                phone_lookup_data = sqlite_plugins.read_sqlite_table(file_path, 'phone_lookup',
                                                                     columns='raw_contact_id, normalized_number')


    contact_data_list = []
    contact_data = dict()

    if raw_contacts_data:
        for entry in raw_contacts_data:
            contact_data['contact_id'] = entry[0]
            contact_data['display_name'] = entry[1]
            contact_data['modified_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[2] / 1000.0))
            for item in phone_lookup_data:
                if item[0] == entry[0]:
                    contact_data['normalized_number'] = item[1]
            contact_data_list.append(contact_data)
            contact_data = dict()

    return contact_data_list

"""
contacts2.db

raw_contacts:
    Contact information on Local Device
    contact_id, display_name, modified_time

accounts:
    Account for local device
    _id, account_name, account_type

phone_lookup:
    Information about phone number
    raw_contact_id, normalized_number

calls:
    Calls Made
    _id, number, date, duration, name, geocoded_location, normalized_number, modified_time, contacts_id, lookup_uri

contacts:
    Contacts
    lookup, _id, photo_id

data:
    contact_id

"""