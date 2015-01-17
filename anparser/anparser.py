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
import logging
import os
import sys
import pandas as pd
import plugins
import plugins.sqlite_plugins


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

    args = parser.parse_args()

    if not os.path.exists(args.evidence) or not os.path.isdir(args.evidence):
        print "Evidence not found...exiting"
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

    # import plugins to process the file listing
    import plugins.sqlite_plugins.android_browser
    import plugins.sqlite_plugins.android_calendar
    import plugins.sqlite_plugins.android_chrome
    import plugins.sqlite_plugins.android_contacts
    import plugins.sqlite_plugins.android_downloads
    import plugins.sqlite_plugins.android_telephony
    import plugins.sqlite_plugins.android_gallery3d
    import plugins.sqlite_plugins.android_media
    import plugins.sqlite_plugins.android_mms
    import plugins.sqlite_plugins.android_vending
    import plugins.sqlite_plugins.google_docs
    import plugins.sqlite_plugins.facebook_katana
    import plugins.sqlite_plugins.facebook_orca
    import plugins.xml_plugins.android_gmail
    import plugins.xml_plugins.android_browser
    import plugins.xml_plugins.android_vending
    import plugins.xml_plugins.google_talk
    import plugins.xml_plugins.snapchat_android
    import plugins.other_plugins.android_gmail_message_parser
    # run plugins

    # Android Browser Parser
    msg = 'Processing Android Browser'
    logging.info(msg)
    print(msg)
    browser_data = plugins.sqlite_plugins.android_browser.android_browser(files_to_process)
    browser_user_defaults, browser_preferences = plugins.xml_plugins.android_browser.android_browser(files_to_process)

    # Android Calendar Parser
    msg = 'Processing Android Calendar'
    logging.info(msg)
    print(msg)
    calendar_data = plugins.sqlite_plugins.android_calendar.android_calendar(files_to_process)

    # Android Chrome Parser
    msg = 'Processing Android Chrome'
    logging.info(msg)
    print(msg)
    chrome_cookies_data, chrome_downloads_data, chrome_history_data = plugins.sqlite_plugins.android_chrome.android_chrome(files_to_process)

    # Android Contact Parser
    msg = 'Processing Android Contacts'
    logging.info(msg)
    print(msg)
    contacts_data = plugins.sqlite_plugins.android_contacts.android_contacts(files_to_process)

    # Android Downloads Parser
    msg = 'Processing Android Downloads'
    logging.info(msg)
    print(msg)
    downloads_data = plugins.sqlite_plugins.android_downloads.android_downloads(files_to_process)

    # Android Gallery3d Parser
    msg = 'Processing Android Gallery3d'
    logging.info(msg)
    print(msg)
    photo_file_data, picasa_data = plugins.sqlite_plugins.android_gallery3d.android_gallery3d(files_to_process)

    # Android Telephony Parser
    msg = 'Processing Android SMS'
    logging.info(msg)
    print(msg)
    telephony_data_sms, telephony_data_threads = \
        plugins.sqlite_plugins.android_telephony.android_telephony(files_to_process)

    # Android Gmail Parser
    msg = 'Processing Android GMail'
    logging.info(msg)
    print(msg)
    gmail_accounts_data = plugins.xml_plugins.android_gmail.android_gmail(files_to_process)

    plugins.other_plugins.android_gmail_message_parser.android_gmail_message_parser(files_to_process, os.path.join(
        args.destination, "Android/Gmail_Messages/"))

    # Android Media Parser
    msg = 'Processing Android Media'
    logging.info(msg)
    print(msg)
    android_media_data = plugins.sqlite_plugins.android_media.android_media(files_to_process)

    # Android MMS Parser
    msg = 'Processing Android MMS'
    logging.info(msg)
    print(msg)
    android_mms_data = plugins.sqlite_plugins.android_mms.android_mms(files_to_process)

    # Android Vending Parser
    msg = 'Processing Android Vending'
    logging.info(msg)
    print(msg)
    vending_library_list, vending_localapp_list, vending_suggestions_list = \
        plugins.sqlite_plugins.android_vending.android_vending(files_to_process)
    vending_data = plugins.xml_plugins.android_vending.android_vending(files_to_process)

    # For XLSX test
    vending_dict = {'android_vending_library':pd.DataFrame(vending_library_list,
                                                           columns=vending_library_list[0].keys()),
                    'android_vending_local_apps':pd.DataFrame(vending_localapp_list,
                                                              columns=vending_localapp_list[0].keys()),
                    'android_vending_suggestions':pd.DataFrame(vending_suggestions_list,
                                                               columns=vending_suggestions_list[0].keys())}

    # Google Docs Parser
    msg = 'Processing Google Docs'
    logging.info(msg)
    print(msg)
    google_docs_account_data, google_docs_collection_data = \
        plugins.sqlite_plugins.google_docs.google_docs(files_to_process)

    # Google Talk Parser
    msg = 'Processing Google Talk'
    logging.info(msg)
    print(msg)
    google_talk_data = plugins.xml_plugins.google_talk.google_talk(files_to_process)

    # Facebook Parser
    msg = 'Processing Facebook'
    logging.info(msg)
    print(msg)
    katana_contact_data, katana_threads_data, katana_msg_data, katana_notifications_data = \
        plugins.sqlite_plugins.facebook_katana.facebook_katana(files_to_process)

    # Facebook Orca (Messenger) Parser
    msg = 'Processing Facebook Messenger'
    logging.info(msg)
    print(msg)
    orca_contact_data, orca_threads_data, orca_msg_data = \
        plugins.sqlite_plugins.facebook_orca.facebook_orca(files_to_process)

    # Snapchat Parser
    msg = 'Processing Snapchat'
    logging.info(msg)
    print(msg)
    snapchat_data = plugins.xml_plugins.snapchat_android.snapchat_android(files_to_process)

    msg = 'Processors Complete'
    logging.info(msg)
    print(msg)
    #
    # End of Plugin Processing
    #

    #
    # Start of Writers
    #
    import writers.csv_writer
    import writers.xlsx_writer

    # Write Contact Data
    msg = 'Writing data to output...'
    logging.info(msg)
    print(msg)
    path = args.destination + '//Android'
    if not os.path.exists(path):
        os.mkdir(path, 0777)
    writers.csv_writer.csv_writer(browser_data, os.path.join(path, 'android_browser.csv'))
    writers.csv_writer.csv_writer(browser_preferences, os.path.join(path, 'android_browser_preferences.csv'))
    writers.csv_writer.csv_writer(browser_user_defaults, os.path.join(path, 'android_browser_user_defaults.csv'))
    writers.csv_writer.csv_writer(calendar_data, os.path.join(path, 'android_calendar.csv'))
    writers.csv_writer.csv_writer(chrome_cookies_data, os.path.join(path, 'android_chrome_cookies.csv'))
    writers.csv_writer.csv_writer(chrome_downloads_data, os.path.join(path, 'android_chrome_downloads.csv'))
    writers.csv_writer.csv_writer(chrome_history_data, os.path.join(path, 'android_chrome_history.csv'))
    writers.csv_writer.csv_writer(contacts_data, os.path.join(path, 'android_contacts.csv'))
    writers.csv_writer.csv_writer(downloads_data, os.path.join(path, 'android_downloads.csv'))
    writers.csv_writer.csv_writer(photo_file_data, os.path.join(path, 'android_gallery3d_files.csv'))
    writers.csv_writer.csv_writer(picasa_data, os.path.join(path, 'android_gallery3d_picasa.csv'))
    writers.csv_writer.csv_writer(android_media_data, os.path.join(path, 'android_media.csv'))
    writers.csv_writer.csv_writer(android_mms_data, os.path.join(path, 'android_mms_glance.csv'))

    # For XLSX Test
    writers.xlsx_writer.xlsx_writer(vending_dict, os.path.join(path, 'android_vending.xlsx'))

    writers.csv_writer.csv_writer(vending_library_list, os.path.join(path, 'android_vending_library.csv'))
    writers.csv_writer.csv_writer(vending_localapp_list, os.path.join(path, 'android_vending_local_apps.csv'))
    writers.csv_writer.csv_writer(vending_suggestions_list, os.path.join(path, 'android_vending_suggestions.csv'))
    writers.csv_writer.csv_writer(vending_data, os.path.join(path, 'android_vending_account_data.csv'))
    writers.csv_writer.csv_writer(telephony_data_sms, os.path.join(path, 'android_telephony_sms.csv'))
    writers.csv_writer.csv_writer(telephony_data_threads, os.path.join(path, 'android_telephony_threads.csv'))
    writers.csv_writer.csv_writer(gmail_accounts_data, os.path.join(path, 'android_gmail_accounts.csv'))

    path = args.destination + '//Google'
    if not os.path.exists(path):
        os.mkdir(path, 0777)
    writers.csv_writer.csv_writer(google_docs_account_data, os.path.join(path, 'google_docs_accounts.csv'))
    writers.csv_writer.csv_writer(google_docs_collection_data, os.path.join(path, 'google_docs_collection.csv'))
    writers.csv_writer.csv_writer(google_talk_data, os.path.join(path, 'google_talk_accounts.csv'))

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

    path = args.destination + '//Snapchat'
    if not os.path.exists(path):
        os.mkdir(path, 0777)
    writers.csv_writer.csv_writer(snapchat_data, os.path.join(path, 'snapchat_preferences.csv'))
    msg = 'Completed'
    logging.info(msg)
    print(msg)