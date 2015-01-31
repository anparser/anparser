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
__date__ = '20150102'
__version__ = '0.00'

# Imports
from collections import OrderedDict
import logging
import os
import sys
import pandas as pd
import plugins
import writers


def scan_for_files(input_dir):
    """
    Iterate across a directory and return a list of files

    :param input_dir: string path to a directory
    :return: Array of relative file paths
    """

    # TODO: Add ability to filter scanned files by name, path or extension

    if os.path.isfile(input_dir):
        return None

    # Initialize Variables
    file_list = []

    # Iterate
    for root, subdir, files in os.walk(input_dir, topdown=True):
        for file_name in files:
            current_file = os.path.join(root, file_name)
            file_list.append(current_file)

    return file_list


if __name__ == "__main__":
    import argparse

    # Handle Command-Line Input
    parser = argparse.ArgumentParser(description="Open Source Android Artifact Parser")

    parser.add_argument('evidence', help='Directory of Android Acquisition')
    parser.add_argument('destination', help='Destination directory to write output files to')
    parser.add_argument('-o', help='Output Type: csv, xlsx', default='csv')
    parser.add_argument('-y', action='store_true', help='Run Yara Malware Signature Scanner', default=False)
    parser.add_argument('-r', help='Run custom command line Yara rule, must run with -y switch')

    args = parser.parse_args()
    if not os.path.exists(args.evidence) or not os.path.isdir(args.evidence):
        print("Evidence not found...exiting")
        sys.exit(1)

    if not os.path.exists(args.destination):
        os.makedirs(args.destination)

    # Sets up Logging
    logging.basicConfig(filename=os.path.join(args.destination, 'anparser.log'), level=logging.DEBUG,
                        format='%(asctime)s | %(levelname)s | %(message)s', filemode='w')
    logging.info('Starting Anparser v' + __version__)
    logging.info('System ' + sys.platform)
    logging.info('Version ' + sys.version)

    # Pre-process files
    files_to_process = scan_for_files(args.evidence)

    #
    # Start of Plugin Processing
    #

    # Run plugins
    # TODO: Complete process of switching parsers to pandas

    # Android Browser Parser
    msg = 'Processing Android Browser'
    logging.info(msg)
    print(msg)
    browser_bookmarks, browser_history = plugins.sqlite_plugins.android_browser.android_browser(files_to_process)
    browser_user_defaults, browser_preferences = plugins.xml_plugins.android_browser.android_browser(files_to_process)

    # Android Calendar Parser
    msg = 'Processing Android Calendar'
    logging.info(msg)
    print(msg)
    calendar_attendees, calendar_events, calendar_reminders, calendar_tasks = \
        plugins.sqlite_plugins.android_calendar.android_calendar(files_to_process)

    # Android Chrome Parser
    msg = 'Processing Android Chrome'
    logging.info(msg)
    print(msg)
    chrome_cookies, chrome_downloads, chrome_keywords, chrome_urls, chrome_visits = \
        plugins.sqlite_plugins.android_chrome.android_chrome(files_to_process)

    # Android Contact Parser
    msg = 'Processing Android Contacts'
    logging.info(msg)
    print(msg)
    contacts_raw, contacts_accounts, contacts_phone = \
        plugins.sqlite_plugins.android_contacts.android_contacts(files_to_process)

    # Android Downloads Parser
    msg = 'Processing Android Downloads'
    logging.info(msg)
    print(msg)
    downloads_data = plugins.sqlite_plugins.android_downloads.android_downloads(files_to_process)

    # Android Emergencymode Parser
    msg = 'Processing Android EmergencyMode'
    logging.info(msg)
    print(msg)
    emergency_data = plugins.sqlite_plugins.android_emergencymode.android_emergencymode(files_to_process)

    # Android Gallery3d Parser
    msg = 'Processing Android Gallery3d'
    logging.info(msg)
    print(msg)
    file_info, gallery_download, gallery_albums, gallery_photos, gallery_users = \
        plugins.sqlite_plugins.android_gallery3d.android_gallery3d(files_to_process)

    # Android Gmail Parser
    msg = 'Processing Android GMail'
    logging.info(msg)
    print(msg)
    gmail_accounts_data = plugins.xml_plugins.android_gmail.android_gmail(files_to_process)

    # Android Logsprovider Parser
    msg = 'Processing Android Logsprovider'
    logging.info(msg)
    print(msg)
    android_logsprovider_data = plugins.sqlite_plugins.android_logsprovider.android_logsprovider(files_to_process)

    # Android Media Parser
    msg = 'Processing Android Media'
    logging.info(msg)
    print(msg)
    external_media, internal_media = plugins.sqlite_plugins.android_media.android_media(files_to_process)


    # Android MMS Parser
    msg = 'Processing Android MMS'
    logging.info(msg)
    print(msg)
    android_mms_events, android_mms_logs = plugins.sqlite_plugins.android_mms.android_mms(files_to_process)

    # Android Telephony Parser
    msg = 'Processing Android SMS'
    logging.info(msg)
    print(msg)
    telephony_data_sms, telephony_data_threads = \
        plugins.sqlite_plugins.android_telephony.android_telephony(files_to_process)

    # Android Vending Parser
    msg = 'Processing Android Vending'
    logging.info(msg)
    print(msg)
    vending_library, vending_localapp, vending_suggestions = \
        plugins.sqlite_plugins.android_vending.android_vending(files_to_process)
    vending_data = plugins.xml_plugins.android_vending.android_vending(files_to_process)


    # Google Docs Parser
    msg = 'Processing Google Docs'
    logging.info(msg)
    print(msg)
    google_docs_account_data, google_docs_collection_data = \
        plugins.sqlite_plugins.google_docs.google_docs(files_to_process)

    if args.o.lower() == 'xlsx':
        google_dict = OrderedDict()
        try:
            google_dict['google_docs_accounts'] = pd.DataFrame(google_docs_account_data,
                                                               columns=google_docs_account_data[0].keys())
        except IndexError:
            pass
        try:
            google_dict['google_docs_collection'] = pd.DataFrame(google_docs_collection_data,
                                                                 columns=google_docs_collection_data[0].keys())
        except IndexError:
            pass

    # Google Talk Parser
    msg = 'Processing Google Talk'
    logging.info(msg)
    print(msg)
    google_talk_data = plugins.xml_plugins.google_talk.google_talk(files_to_process)

    if args.o.lower() == 'xlsx':
        try:
            google_dict['google_talk_accounts'] = pd.DataFrame(google_talk_data,
                                                               columns=google_talk_data[0].keys())
        except IndexError:
            pass

    # Google Plus Parser
    msg = 'Processing Google Plus'
    logging.info(msg)
    print(msg)
    google_plus_photos, google_plus_contacts, google_plus_guns = \
        plugins.sqlite_plugins.google_plus.google_plus(files_to_process)
    google_plus_accounts = plugins.xml_plugins.google_plus.google_plus(files_to_process)

    if args.o.lower() == 'xlsx':
        try:
            google_dict['google_plus_photos'] = pd.DataFrame(google_plus_photos,
                                                               columns=google_plus_photos[0].keys())
        except IndexError:
            pass
        try:
            google_dict['google_plus_contacts'] = pd.DataFrame(google_plus_contacts,
                                                               columns=google_plus_contacts[0].keys())
        except IndexError:
            pass
        try:
            google_dict['google_plus_guns'] = pd.DataFrame(google_plus_guns,
                                                               columns=google_plus_guns[0].keys())
        except IndexError:
            pass
        try:
            google_dict['google_plus_accounts'] = pd.DataFrame(google_plus_accounts,
                                                               columns=google_plus_accounts[0].keys())
        except IndexError:
            pass

    # Facebook Parser
    msg = 'Processing Facebook'
    logging.info(msg)
    print(msg)
    katana_contact_data, katana_threads_data, katana_msg_data, katana_notifications_data = \
        plugins.sqlite_plugins.facebook_katana.facebook_katana(files_to_process)

    if args.o.lower() == 'xlsx':
        facebook_dict = OrderedDict()
        try:
            facebook_dict['facebook_katana_contacts'] = pd.DataFrame(katana_contact_data,
                                                               columns=katana_contact_data[0].keys())
        except IndexError:
            pass
        try:
            facebook_dict['facebook_katana_threads'] = pd.DataFrame(katana_threads_data,
                                                                 columns=katana_threads_data[0].keys())
        except IndexError:
            pass
        try:
            facebook_dict['facebook_katana_messages'] = pd.DataFrame(katana_msg_data,
                                                               columns=katana_msg_data[0].keys())
        except IndexError:
            pass
        try:
            facebook_dict['facebook_katana_notifications'] = pd.DataFrame(katana_notifications_data,
                                                                 columns=katana_notifications_data[0].keys())
        except IndexError:
            pass

    # Facebook Orca (Messenger) Parser
    msg = 'Processing Facebook Messenger'
    logging.info(msg)
    print(msg)
    orca_contact_data, orca_threads_data, orca_msg_data = \
        plugins.sqlite_plugins.facebook_orca.facebook_orca(files_to_process)

    if args.o.lower() == 'xlsx':
        try:
            facebook_dict['facebook_orca_contacts'] = pd.DataFrame(orca_contact_data,
                                                               columns=orca_contact_data[0].keys())
        except IndexError:
            pass
        try:
            facebook_dict['facebook_orca_threads'] = pd.DataFrame(orca_threads_data,
                                                                 columns=orca_threads_data[0].keys())
        except IndexError:
            pass
        try:
            facebook_dict['facebook_orca_messages'] = pd.DataFrame(orca_msg_data,
                                                               columns=orca_msg_data[0].keys())
        except IndexError:
            pass

    # Kik Messenger Parser
    msg = 'Processing Kik Messenger'
    logging.info(msg)
    print(msg)
    kik_contact_data, kik_chat_data = plugins.sqlite_plugins.kik_android.kik_android(files_to_process)
    kik_preferences_data = plugins.xml_plugins.kik_android.kik_android(files_to_process)

    if args.o.lower() == 'xlsx':
        kik_dict = OrderedDict()
        try:
            kik_dict['kik_contacts'] = pd.DataFrame(kik_contact_data,
                                                    columns=kik_contact_data[0].keys())
        except IndexError:
            pass
        try:
            kik_dict['kik_chat'] = pd.DataFrame(kik_chat_data,
                                                columns=kik_chat_data[0].keys())
        except IndexError:
            pass
        try:
            kik_dict['kik_preferences'] = pd.DataFrame(kik_preferences_data,
                                                       columns=kik_preferences_data[0].keys())
        except IndexError:
            pass

    # Samsung Galaxyfinder Parser
    msg = 'Processing Samsung Galaxyfinder'
    logging.info(msg)
    print(msg)
    samsung_galaxyfinder_data = plugins.sqlite_plugins.samsung_galaxyfinder.samsung_galaxyfinder(files_to_process)

    if args.o.lower() == 'xlsx':
        samsung_dict = OrderedDict()
        try:
            samsung_dict['samsung_galaxyfinder'] = pd.DataFrame(samsung_galaxyfinder_data,
                                                                columns=samsung_galaxyfinder_data[0].keys())
        except IndexError:
            pass

    # Snapchat Parser
    msg = 'Processing Snapchat'
    logging.info(msg)
    print(msg)
    snapchat_friends_data, snapchat_chat_data, snapchat_viewing_data, snapchat_files_data = \
        plugins.sqlite_plugins.snapchat_android.snapchat_android(files_to_process)
    snapchat_preferences_data = plugins.xml_plugins.snapchat_android.snapchat_android(files_to_process)

    if args.o.lower() == 'xlsx':
        snapchat_dict = OrderedDict()
        try:
            snapchat_dict['snapchat_friends'] = pd.DataFrame(snapchat_friends_data,
                                                             columns=snapchat_friends_data[0].keys())
        except IndexError:
            pass
        try:
            snapchat_dict['snapchat_chat'] = pd.DataFrame(snapchat_chat_data,
                                                          columns=snapchat_chat_data[0].keys())
        except IndexError:
            pass
        try:
            snapchat_dict['snapchat_viewing'] = pd.DataFrame(snapchat_viewing_data,
                                                             columns=snapchat_viewing_data[0].keys())
        except IndexError:
            pass
        try:
            snapchat_dict['snapchat_files'] = pd.DataFrame(snapchat_files_data,
                                                           columns=snapchat_files_data[0].keys())
        except IndexError:
            pass
        try:
            snapchat_dict['snapchat_preferences'] = pd.DataFrame(snapchat_preferences_data,
                                                                 columns=snapchat_preferences_data[0].keys())
        except IndexError:
            pass

    # Teslacoilsw Launcer Parser
    msg = 'Processing Teslacoilsw'
    logging.info(msg)
    print(msg)
    tesla_allapps_data, tesla_favorites_data = \
        plugins.sqlite_plugins.teslacoilsw_launcher.teslacoilsw_launcher(files_to_process)

    if args.o.lower() == 'xlsx':
        tesla_dict = OrderedDict()
        try:
            tesla_dict['teslacoilsw_all_apps'] = pd.DataFrame(tesla_allapps_data,
                                                              columns=tesla_allapps_data[0].keys())
        except IndexError:
            pass
        try:
            tesla_dict['teslacoilsw_favorites'] = pd.DataFrame(tesla_favorites_data,
                                                               columns=tesla_favorites_data[0].keys())
        except IndexError:
            pass

    # Valve Parser
    msg = 'Processing Valve'
    logging.info(msg)
    print(msg)
    valve_friends_data, valve_chat_data, valve_debug_data = \
        plugins.sqlite_plugins.valvesoftware_android.valvesoftware_android(files_to_process)
    valve_preferences_data = plugins.xml_plugins.valvesoftware_android.valvesoftware_android(files_to_process)

    if args.o.lower() == 'xlsx':
        valve_dict = OrderedDict()
        try:
            valve_dict['valve_friends'] = pd.DataFrame(valve_friends_data,
                                                             columns=valve_friends_data[0].keys())
        except IndexError:
            pass
        try:
            valve_dict['valve_chat'] = pd.DataFrame(valve_chat_data,
                                                          columns=valve_chat_data[0].keys())
        except IndexError:
            pass
        try:
            valve_dict['valve_debug'] = pd.DataFrame(valve_debug_data,
                                                             columns=valve_debug_data[0].keys())
        except IndexError:
            pass
        try:
            valve_dict['valve_preferences'] = pd.DataFrame(valve_preferences_data,
                                                                 columns=valve_preferences_data[0].keys())
        except IndexError:
            pass

    # Vlingo Midas Parser
    msg = 'Processing Vlingo Midas'
    logging.info(msg)
    print(msg)
    vlingo_contacts_data = plugins.sqlite_plugins.vlingo_midas.vlingo_midas(files_to_process)

    if args.o.lower() == 'xlsx':
        vlingo_dict = OrderedDict()
        try:
            vlingo_dict['vlingo_midas_contacts'] = pd.DataFrame(vlingo_contacts_data,
                                                                columns=vlingo_contacts_data[0].keys())
        except IndexError:
            pass

    # Yara Malware Parser
    if args.y:
        msg = 'Running Yara Malware Scanner'
        logging.info(msg)
        print(msg)
        if args.r:
            yara_data = plugins.other_plugins.yara_parser.yara_parser(files_to_process, args.r)
        else:
            yara_data = plugins.other_plugins.yara_parser.yara_parser(files_to_process)

        if args.o.lower() == 'xlsx':
            yara_dict = OrderedDict()
            try:
                yara_dict['yara_matches'] = pd.DataFrame(yara_data,
                                                         columns=yara_data[0].keys())
            except IndexError:
                pass

    msg = 'Processors Complete'
    logging.info(msg)
    print(msg)
    #
    # End of Plugin Processing
    #

    #
    # Start of Writers
    #

    msg = 'Writing data to output...'
    logging.info(msg)
    print(msg)

    # Write Contact Data
    # TODO: Recreate CSV writer instead of calling .to_csv manually.
    # TODO: Check the None type errors from the try/except items below.
    # TODO: Add back in xlsx support w/ pandas.
    # TODO: Add database path to pandas dataset.
    # TODO: Convert timestamps in pandas dataset.

    if args.o.lower() == 'csv':
        path = args.destination + '//Android'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        browser_bookmarks.to_csv(os.path.join(path, 'android_browser_bookmarks.csv'), '|')
        browser_history.to_csv(os.path.join(path, 'android_browser_history.csv'), '|')

        writers.csv_writer.csv_writer(browser_preferences, os.path.join(path, 'android_browser_preferences.csv'))
        writers.csv_writer.csv_writer(browser_user_defaults, os.path.join(path, 'android_browser_user_defaults.csv'))

        calendar_attendees.to_csv(os.path.join(path, 'android_calendar_attendees.csv'), '|')
        try:
            calendar_events.to_csv(os.path.join(path, 'android_calendar_events.csv'), '|')
        except AttributeError:
            pass
        calendar_reminders.to_csv(os.path.join(path, 'android_calendar_reminders.csv'), '|')
        calendar_tasks.to_csv(os.path.join(path, 'android_calendar_tasks.csv'), '|')
        chrome_cookies.to_csv(os.path.join(path, 'android_chrome_cookies.csv'), '|')
        try:
            chrome_downloads.to_csv(os.path.join(path, 'android_chrome_downloads.csv'), '|')
        except AttributeError:
            pass
        chrome_keywords.to_csv(os.path.join(path, 'android_chrome_keywords.csv'), '|')
        chrome_urls.to_csv(os.path.join(path, 'android_chrome_urls.csv'), '|', encoding='utf-8')
        chrome_visits.to_csv(os.path.join(path, 'android_chrome_visits.csv'), '|')
        try:
            contacts_raw.to_csv(os.path.join(path, 'android_contacts_rawcontacts.csv'), '|')
        except AttributeError:
            pass
        contacts_accounts.to_csv(os.path.join(path, 'android_contacts_accounts.csv'), '|')
        try:
            contacts_phone.to_csv(os.path.join(path, 'android_contacts_phonelookup.csv'), '|')
        except AttributeError:
            pass
        downloads_data.to_csv(os.path.join(path, 'android_downloads.csv'), '|')
        emergency_data.to_csv(os.path.join(path, 'android_emergencymode.csv'), '|')
        file_info.to_csv(os.path.join(path, 'android_gallery3d_fileinfo.csv'), '|')
        gallery_download.to_csv(os.path.join(path, 'android_gallery3d_downloads.csv'), '|')
        gallery_albums.to_csv(os.path.join(path, 'android_gallery3d_albums.csv'), '|')
        gallery_photos.to_csv(os.path.join(path, 'android_gallery3d_photos.csv'), '|')
        gallery_users.to_csv(os.path.join(path, 'android_gallery3d_users.csv'), '|')

        writers.csv_writer.csv_writer(gmail_accounts_data, os.path.join(path, 'android_gmail_accounts.csv'))

        android_logsprovider_data.to_csv(os.path.join(path, 'android_logsprovider.csv'), '|', encoding='utf-8')
        external_media.to_csv(os.path.join(path, 'android_media_external.csv'), '|')
        internal_media.to_csv(os.path.join(path, 'android_media_internal.csv'), '|')
        android_mms_events.to_csv(os.path.join(path, 'android_mms_events.csv'), '|')
        android_mms_logs.to_csv(os.path.join(path, 'android_mms_logs.csv'), '|')
        telephony_data_sms.to_csv(os.path.join(path, 'android_telephony_sms.csv'), '|')
        telephony_data_threads.to_csv(os.path.join(path, 'android_telephony_threads.csv'), '|')
        try:
            vending_library.to_csv(os.path.join(path, 'android_vending_library.csv'), '|')
        except AttributeError:
            pass
        try:
            vending_localapp.to_csv(os.path.join(path, 'android_vending_localapps.csv'), '|')
        except AttributeError:
            pass
        vending_suggestions.to_csv(os.path.join(path, 'android_vending_suggestions.csv'), '|')

        writers.csv_writer.csv_writer(vending_data, os.path.join(path, 'android_vending_account_data.csv'))

        path = args.destination + '//Google'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.csv_writer.csv_writer(google_docs_account_data, os.path.join(path, 'google_docs_accounts.csv'))
        writers.csv_writer.csv_writer(google_docs_collection_data, os.path.join(path, 'google_docs_collection.csv'))
        writers.csv_writer.csv_writer(google_talk_data, os.path.join(path, 'google_talk_accounts.csv'))
        writers.csv_writer.csv_writer(google_plus_accounts, os.path.join(path, 'google_plus_accounts.csv'))
        writers.csv_writer.csv_writer(google_plus_photos, os.path.join(path, 'google_plus_photos.csv'))
        writers.csv_writer.csv_writer(google_plus_contacts, os.path.join(path, 'google_plus_contacts.csv'))
        writers.csv_writer.csv_writer(google_plus_guns, os.path.join(path, 'google_plus_guns.csv'))


        path = args.destination + '//Facebook'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.csv_writer.csv_writer(katana_contact_data, os.path.join(path, 'facebook_katana_contacts.csv'))
        writers.csv_writer.csv_writer(katana_threads_data, os.path.join(path, 'facebook_katana_threads.csv'))
        writers.csv_writer.csv_writer(katana_msg_data, os.path.join(path, 'facebook_katana_messages.csv'))
        writers.csv_writer.csv_writer(katana_notifications_data, os.path.join(path, 'facebook_katana_notifications.csv'))
        writers.csv_writer.csv_writer(orca_contact_data, os.path.join(path, 'facebook_orca_contacts.csv'))
        writers.csv_writer.csv_writer(orca_threads_data, os.path.join(path, 'facebook_orca_threads.csv'))
        writers.csv_writer.csv_writer(orca_msg_data, os.path.join(path, 'facebook_orca_messages.csv'))

        path = args.destination + '//Kik'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.csv_writer.csv_writer(kik_contact_data, os.path.join(path, 'kik_contacts.csv'))
        writers.csv_writer.csv_writer(kik_chat_data, os.path.join(path, 'kik_chat.csv'))
        writers.csv_writer.csv_writer(kik_preferences_data, os.path.join(path, 'kik_preferences.csv'))

        path = args.destination + '//Samsung'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.csv_writer.csv_writer(samsung_galaxyfinder_data, os.path.join(path, 'samsung_galaxyfinder.csv'))

        path = args.destination + '//Snapchat'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.csv_writer.csv_writer(snapchat_friends_data, os.path.join(path, 'snapchat_friends.csv'))
        writers.csv_writer.csv_writer(snapchat_chat_data, os.path.join(path, 'snapchat_chat.csv'))
        writers.csv_writer.csv_writer(snapchat_viewing_data, os.path.join(path, 'snapchat_viewingsessions.csv'))
        writers.csv_writer.csv_writer(snapchat_files_data, os.path.join(path, 'snapchat_files.csv'))
        writers.csv_writer.csv_writer(snapchat_preferences_data, os.path.join(path, 'snapchat_preferences.csv'))

        path = args.destination + '//Teslacoilsw'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.csv_writer.csv_writer(tesla_allapps_data, os.path.join(path, 'teslacoilsw_allapps.csv'))
        writers.csv_writer.csv_writer(tesla_favorites_data, os.path.join(path, 'teslacoilsw_favorites.csv'))

        path = args.destination + '//Valve'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.csv_writer.csv_writer(valve_friends_data, os.path.join(path, 'valve_friends.csv'))
        writers.csv_writer.csv_writer(valve_chat_data, os.path.join(path, 'valve_chat.csv'))
        writers.csv_writer.csv_writer(valve_debug_data, os.path.join(path, 'valve_debug.csv'))
        writers.csv_writer.csv_writer(valve_preferences_data, os.path.join(path, 'valve_preferences.csv'))

        path = args.destination + '//Vlingo'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.csv_writer.csv_writer(vlingo_contacts_data, os.path.join(path, 'vlingo_midas_contacts.csv'))

        if args.y:
            path = args.destination + '//Yara'
            if not os.path.exists(path):
                os.mkdir(path, 0777)
            writers.csv_writer.csv_writer(yara_data, os.path.join(path, 'yara_matches.csv'))

        '''
        path = args.destination + '//Google'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.xlsx_writer.xlsx_writer(google_dict, os.path.join(path, 'google.xlsx'))

        path = args.destination + '//Facebook'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.xlsx_writer.xlsx_writer(facebook_dict, os.path.join(path, 'facebook.xlsx'))

        path = args.destination + '//Kik'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.xlsx_writer.xlsx_writer(kik_dict, os.path.join(path, 'kik.xlsx'))

        path = args.destination + '//Samsung'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.xlsx_writer.xlsx_writer(samsung_dict, os.path.join(path, 'samsung.xlsx'))

        path = args.destination + '//Snapchat'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.xlsx_writer.xlsx_writer(snapchat_dict, os.path.join(path, 'snapchat.xlsx'))

        path = args.destination + '//Teslacoilsw'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.xlsx_writer.xlsx_writer(tesla_dict, os.path.join(path, 'teslacoilsw.xlsx'))

        path = args.destination + '//Valve'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.xlsx_writer.xlsx_writer(valve_dict, os.path.join(path, 'valve.xlsx'))

        path = args.destination + '//Vlingo'
        if not os.path.exists(path):
            os.mkdir(path, 0777)
        writers.xlsx_writer.xlsx_writer(vlingo_dict, os.path.join(path, 'vlingo.xlsx'))

        if args.y:
            path = args.destination + '//Yara'
            if not os.path.exists(path):
                os.mkdir(path, 0777)
            writers.xlsx_writer.xlsx_writer(yara_dict, os.path.join(path, 'yara.xlsx'))'''
    msg = 'Completed'
    logging.info(msg)
    print(msg)