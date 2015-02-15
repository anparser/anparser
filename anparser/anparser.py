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
            current_file = current_file.decode('utf-8')
            file_list.append(current_file)

    return file_list


if __name__ == "__main__":
    import argparse

    # Handle Command-Line Input
    parser = argparse.ArgumentParser(description="Open Source Android Artifact Parser")

    parser.add_argument('evidence', help='Directory of Android Acquisition')
    parser.add_argument('destination', help='Destination directory to write output files to')
    parser.add_argument('-o', help='Output Type: csv, xlsx', default='csv')
    parser.add_argument('-y', help='Provide file path to custom Yara rules and run Yara')
    parser.add_argument('-s', help='Regular expression searching - supply file path with new line separated '
                                   'searches or type a single search')

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
    # TODO: Add in the android_gmail_message_extractor & parser
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

    # Facebook Parser
    msg = 'Processing Facebook'
    logging.info(msg)
    print(msg)
    katana_contact, katana_folder_count, katana_folder, katana_msg, katana_thread_user,\
    katana_threads, katana_notifications = plugins.sqlite_plugins.facebook_katana.facebook_katana(files_to_process)

    # Facebook Orca (Messenger) Parser
    msg = 'Processing Facebook Messenger'
    logging.info(msg)
    print(msg)
    orca_contact, orca_folder_count, orca_folder, orca_msg, orca_thread_user, orca_threads = \
        plugins.sqlite_plugins.facebook_orca.facebook_orca(files_to_process)

 # Google Docs Parser
    msg = 'Processing Google Docs'
    logging.info(msg)
    print(msg)
    google_docs_account, google_docs_collection, google_docs_contains, google_docs_entry = \
        plugins.sqlite_plugins.google_docs.google_docs(files_to_process)

    # Google Talk Parser
    msg = 'Processing Google Talk'
    logging.info(msg)
    print(msg)
    google_talk_data = plugins.xml_plugins.google_talk.google_talk(files_to_process)

    # Google Plus Parser
    msg = 'Processing Google Plus'
    logging.info(msg)
    print(msg)
    google_plus_photos, google_plus_contacts_search, google_plus_contacts, google_plus_guns = \
        plugins.sqlite_plugins.google_plus.google_plus(files_to_process)
    google_plus_accounts = plugins.xml_plugins.google_plus.google_plus(files_to_process)

    # Infraware Polaris Parser
    msg = 'Processing Infraware Polaris'
    logging.info(msg)
    print(msg)
    polaris_contacts, polaris_files, polaris_attendee, polaris_shared, polaris_messages = \
        plugins.sqlite_plugins.infraware_office.infraware_office(files_to_process)
    polaris_preferences = plugins.xml_plugins.infraware_office.infraware_office(files_to_process)

    # Kik Messenger Parser
    msg = 'Processing Kik Messenger'
    logging.info(msg)
    print(msg)
    kik_content, kik_contact, kik_messages = plugins.sqlite_plugins.kik_android.kik_android(files_to_process)
    kik_preferences_data = plugins.xml_plugins.kik_android.kik_android(files_to_process)

    # Samsung Galaxyfinder Parser
    msg = 'Processing Samsung Galaxyfinder'
    logging.info(msg)
    print(msg)
    galaxyfinder_content, galaxyfinder_tagging, galaxyfinder_tags =\
        plugins.sqlite_plugins.samsung_galaxyfinder.samsung_galaxyfinder(files_to_process)

    # Skype Raider Parser
    msg = 'Processing Skype'
    logging.info(msg)
    print(msg)
    skype_accounts, skype_call_members, skype_calls, skype_chat_members, skype_chat, skype_contacts,\
        skype_conversations, skype_media, skype_messages, skype_participants, skype_transfers =\
        plugins.sqlite_plugins.skype_raider.skype_raider(files_to_process)

    # Snapchat Parser
    msg = 'Processing Snapchat'
    logging.info(msg)
    print(msg)
    snapchat_chat, snapchat_conversation, snapchat_friends, snapchat_storyfiles, snapchat_recvsnaps,\
    snapchat_sentsnaps, snapchat_images, snapchat_videos, snapchat_viewing = \
        plugins.sqlite_plugins.snapchat_android.snapchat_android(files_to_process)
    snapchat_preferences = plugins.xml_plugins.snapchat_android.snapchat_android(files_to_process)

    # Teslacoilsw Launcer Parser
    msg = 'Processing Teslacoilsw'
    logging.info(msg)
    print(msg)
    tesla_allapps, tesla_favorites = \
        plugins.sqlite_plugins.teslacoilsw_launcher.teslacoilsw_launcher(files_to_process)

    # Valve Parser
    msg = 'Processing Valve'
    logging.info(msg)
    print(msg)
    valve_friends, valve_chat, valve_debug = \
        plugins.sqlite_plugins.valvesoftware_android.valvesoftware_android(files_to_process)
    valve_preferences = plugins.xml_plugins.valvesoftware_android.valvesoftware_android(files_to_process)

    # Venmo Parser
    msg = 'Processing Venmo'
    logging.info(msg)
    print(msg)
    venmo_comments, venmo_stories, venmo_people, venmo_users = plugins.sqlite_plugins.venmo.venmo(files_to_process)
    venmo_preferences = plugins.xml_plugins.venmo.venmo(files_to_process)

    # Vlingo Midas Parser
    msg = 'Processing Vlingo Midas'
    logging.info(msg)
    print(msg)
    vlingo_contacts = plugins.sqlite_plugins.vlingo_midas.vlingo_midas(files_to_process)

    # Whisper Parser
    msg = 'Processing Whisper'
    logging.info(msg)
    print(msg)
    whisper_conversations, whisper_messages, whisper_whispers, whisper_groups, whisper_notifications = \
        plugins.sqlite_plugins.sh_whisper.sh_whisper(files_to_process)
    whisper_preferences = plugins.xml_plugins.sh_whisper.sh_whisper(files_to_process)

    # Yara Malware Parser
    if args.y:
        msg = 'Running Yara Malware Scanner'
        logging.info(msg)
        print(msg)
        try:
            yara_data = plugins.other_plugins.yara_parser.yara_parser(files_to_process, args.y)
        except IOError:
            pass

    # RegEx Searches
    if args.s:
        msg = 'Running Search module'
        logging.info(msg)
        print(msg)
        search_data = plugins.other_plugins.search_parser.search_parser(files_to_process, args.s)

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

    android_dict = {}
    facebook_dict = {}
    google_dict = {}
    infraware_dict = {}
    kik_dict = {}
    samsung_dict = {}
    skype_dict = {}
    snapchat_dict = {}
    tesla_dict = {}
    valve_dict = {}
    venmo_dict = {}
    vlingo_dict = {}
    whisper_dict = {}
    yara_dict = {}
    search_dict = {}

    android_path = args.destination + '//Android'
    android_dict['android_browser_bookmarks'] = browser_bookmarks
    android_dict['android_browser_history'] = browser_history
    android_dict['android_browser_preferences'] = browser_preferences
    android_dict['android_browser_user_defaults'] = browser_user_defaults
    android_dict['android_calendar_attendees'] = calendar_attendees
    android_dict['android_calendar_events'] = calendar_events
    android_dict['android_calendar_reminders'] = calendar_reminders
    android_dict['android_calendar_tasks'] = calendar_tasks
    android_dict['android_chrome_cookies'] = chrome_cookies
    android_dict['android_chrome_downloads'] = chrome_downloads
    android_dict['android_chrome_keywords'] = chrome_keywords
    android_dict['android_chrome_urls'] = chrome_urls
    android_dict['android_chrome_visits'] = chrome_visits
    android_dict['android_contacts_rawcontacts'] = contacts_raw
    android_dict['android_contacts_accounts'] = contacts_accounts
    android_dict['android_contacts_phonelookup'] = contacts_phone
    android_dict['android_downloads'] = downloads_data
    android_dict['android_emergencymode'] = emergency_data
    android_dict['android_gallery3d_fileinfo'] = file_info
    android_dict['android_gallery3d_downloads'] = gallery_download
    android_dict['android_gallery3d_albums'] = gallery_albums
    android_dict['android_gallery3d_photos'] = gallery_photos
    android_dict['android_gallery3d_users'] = gallery_users
    android_dict['android_gmail_accounts'] = gmail_accounts_data
    android_dict['android_logsprovider'] = android_logsprovider_data
    android_dict['android_media_external'] = external_media
    android_dict['android_media_internal'] = internal_media
    android_dict['android_mms_events'] = android_mms_events
    android_dict['android_mms_logs'] = android_mms_logs
    android_dict['android_telephony_sms'] = telephony_data_sms
    android_dict['android_telephony_threads'] = telephony_data_threads
    android_dict['android_vending_accounts'] = vending_data
    android_dict['android_vending_library'] = vending_library
    android_dict['android_vending_localapps'] = vending_localapp
    android_dict['android_vending_suggestions'] = vending_suggestions

    facebook_path = args.destination + '//Facebook'

    facebook_dict['facebook_katana_contacts'] = katana_contact
    facebook_dict['facebook_katana_folder_count'] = katana_folder_count
    facebook_dict['facebook_katana_folder'] = katana_folder
    facebook_dict['facebook_katana_messages'] = katana_msg
    facebook_dict['facebook_katana_thread_users'] = katana_thread_user
    facebook_dict['facebook_katana_threads'] = katana_threads
    facebook_dict['facebook_katana_notifications'] = katana_notifications
    facebook_dict['facebook_orca_contacts'] = orca_contact
    facebook_dict['facebook_orca_folder_count'] = orca_folder_count
    facebook_dict['facebook_orca_folder'] = orca_folder
    facebook_dict['facebook_orca_messages'] = orca_msg
    facebook_dict['facebook_orca_thread_users'] = orca_thread_user
    facebook_dict['facebook_orca_threads'] = orca_threads

    google_path = args.destination + '//Google'

    google_dict['google_docs_accounts'] = google_docs_account
    google_dict['google_docs_collection'] = google_docs_collection
    google_dict['google_docs_contains'] = google_docs_contains
    google_dict['google_docs_entry'] = google_docs_entry
    google_dict['google_talk_accounts'] = google_talk_data
    google_dict['google_plus_accounts'] = google_plus_accounts
    google_dict['google_plus_photos'] = google_plus_photos
    google_dict['google_plus_contact_search'] = google_plus_contacts_search
    google_dict['google_plus_contacts'] = google_plus_contacts
    google_dict['google_plus_guns'] = google_plus_guns

    infraware_path = args.destination + '//Infraware'

    infraware_dict['polaris_contacts'] = polaris_contacts
    infraware_dict['polaris_files'] = polaris_files
    infraware_dict['polaris_attendees'] = polaris_attendee
    infraware_dict['polaris_shared_files'] = polaris_shared
    infraware_dict['polaris_messages'] = polaris_messages
    infraware_dict['polaris_preferences'] = polaris_preferences

    kik_path = args.destination + '//Kik'

    kik_dict['kik_content'] = kik_content
    kik_dict['kik_contacts'] = kik_contact
    kik_dict['kik_messages'] = kik_messages
    kik_dict['kik_preferences'] = kik_preferences_data

    samsung_path = args.destination + '//Samsung'

    samsung_dict['samsung_galaxyfinder_content'] = galaxyfinder_content
    samsung_dict['samsung_galaxyfinder_tagging'] = galaxyfinder_tagging
    samsung_dict['samsung_galaxyfinder_tags'] = galaxyfinder_tags

    skype_path = args.destination + '//Skype'

    skype_dict['skype_raider_accounts'] = skype_accounts
    skype_dict['skype_raider_call_members'] = skype_call_members
    skype_dict['skype_raider_calls'] = skype_calls
    skype_dict['skype_raider_chat_members'] = skype_chat_members
    skype_dict['skype_raider_chats'] = skype_chat
    skype_dict['skype_raider_contacts'] = skype_contacts
    skype_dict['skype_raider_conversations'] = skype_conversations
    skype_dict['skype_raider_media'] = skype_media
    skype_dict['skype_raider_messages'] = skype_messages
    skype_dict['skype_raider_participants'] = skype_participants
    skype_dict['skype_raider_media_transfers'] = skype_transfers

    snapchat_path = args.destination + '//Snapchat'

    snapchat_dict['snapchat_chat'] = snapchat_chat
    snapchat_dict['snapchat_conversation'] = snapchat_conversation
    snapchat_dict['snapchat_friends'] = snapchat_friends
    snapchat_dict['snapchat_storyfiles'] = snapchat_storyfiles
    snapchat_dict['snapchat_recvsnaps'] = snapchat_recvsnaps
    snapchat_dict['snapchat_sentsnaps'] = snapchat_sentsnaps
    snapchat_dict['snapchat_images'] = snapchat_images
    snapchat_dict['snapchat_videos'] = snapchat_videos
    snapchat_dict['snapchat_viewingsessions'] = snapchat_viewing
    snapchat_dict['snapchat_preferences'] = snapchat_preferences

    tesla_path = args.destination + '//Teslacoilsw'

    tesla_dict['teslacoilsw_allapps'] = tesla_allapps
    tesla_dict['teslacoilsw_favorites'] = tesla_favorites

    valve_path = args.destination + '//Valve'

    valve_dict['valve_friends'] = valve_friends
    valve_dict['valve_chat'] = valve_chat
    valve_dict['valve_debug'] = valve_debug
    valve_dict['valve_preferences'] = valve_preferences

    venmo_path = args.destination + '//Venmo'

    venmo_dict['venmo_comments'] = venmo_comments
    venmo_dict['venmo_stories'] = venmo_stories
    venmo_dict['venmo_people'] = venmo_people
    venmo_dict['venmo_users'] = venmo_users
    venmo_dict['venmo_preferences'] = venmo_preferences

    vlingo_path = args.destination + '//Vlingo'

    vlingo_dict['vlingo_midas_contacts'] = vlingo_contacts

    whisper_path = args.destination + '//Whisper'

    whisper_dict['whisper_conversations'] = whisper_conversations
    whisper_dict['whisper_messages'] = whisper_messages
    whisper_dict['whisper_posts'] = whisper_whispers
    whisper_dict['whisper_groups'] = whisper_groups
    whisper_dict['whisper_notifications'] = whisper_notifications
    whisper_dict['whisper_preferences'] = whisper_preferences

    if args.y:
        yara_path = args.destination + '//Yara'

        try:
            yara_dict['yara_matches'] = yara_data
        except NameError:
            pass

    if args.s:
        search_path = args.destination + '//Search'

        try:
            search_dict['search_matches'] = search_data
        except NameError:
            pass

    if args.o.lower() == 'csv':
        writers.csv_writer.csv_writer(android_dict, android_path)
        writers.csv_writer.csv_writer(facebook_dict, facebook_path)
        writers.csv_writer.csv_writer(google_dict, google_path)
        writers.csv_writer.csv_writer(infraware_dict, infraware_path)
        writers.csv_writer.csv_writer(kik_dict, kik_path)
        writers.csv_writer.csv_writer(samsung_dict, samsung_path)
        writers.csv_writer.csv_writer(skype_dict, skype_path)
        writers.csv_writer.csv_writer(snapchat_dict, snapchat_path)
        writers.csv_writer.csv_writer(tesla_dict, tesla_path)
        writers.csv_writer.csv_writer(valve_dict, valve_path)
        writers.csv_writer.csv_writer(venmo_dict, venmo_path)
        writers.csv_writer.csv_writer(vlingo_dict, vlingo_path)
        writers.csv_writer.csv_writer(whisper_dict, whisper_path)
        if yara_dict != {}:
            writers.csv_writer.csv_writer(yara_dict, yara_path)
        if search_dict != {}:
            writers.csv_writer.csv_writer(search_dict, search_path)
    else:
        writers.xlsx_writer.xlsx_writer(android_dict, android_path, 'android.xlsx')
        writers.xlsx_writer.xlsx_writer(facebook_dict, facebook_path, 'facebook.xlsx')
        writers.xlsx_writer.xlsx_writer(google_dict, google_path, 'google.xlsx')
        writers.xlsx_writer.xlsx_writer(infraware_dict, infraware_path, 'infraware.xlsx')
        writers.xlsx_writer.xlsx_writer(kik_dict, kik_path, 'kik.xlsx')
        writers.xlsx_writer.xlsx_writer(samsung_dict, samsung_path, 'samsung.xlsx')
        writers.xlsx_writer.xlsx_writer(skype_dict, skype_path, 'skype.xlsx')
        writers.xlsx_writer.xlsx_writer(snapchat_dict, snapchat_path, 'snapchat.xlsx')
        writers.xlsx_writer.xlsx_writer(tesla_dict, tesla_path, 'teslacoilsw.xlsx')
        writers.xlsx_writer.xlsx_writer(valve_dict, valve_path, 'valve.xlsx')
        writers.xlsx_writer.xlsx_writer(venmo_dict, venmo_path, 'venmo.xlsx')
        writers.xlsx_writer.xlsx_writer(vlingo_dict, vlingo_path, 'vlingo.xlsx')
        writers.xlsx_writer.xlsx_writer(whisper_dict, whisper_path, 'whisper.xlsx')
        if yara_dict != {}:
            writers.xlsx_writer.xlsx_writer(yara_dict, yara_path, 'yara.xlsx')
        if search_dict != {}:
            writers.xlsx_writer.xlsx_writer(search_dict, search_path, 'search.xlsx')

    msg = 'Completed'
    logging.info(msg)
    print(msg)