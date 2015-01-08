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

    # Sets up Logging
    logging.basicConfig(filename='anparser.log', level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
    logging.info('Starting Anparser v' + __version__)
    logging.info('System ' + sys.platform)
    logging.info('Version ' + sys.version)

    if not os.path.exists(args.evidence) or not os.path.isdir(args.evidence):
        print "Evidence not found...exiting"
        sys.exit(1)

    if not os.path.exists(args.destination):
        os.makedirs(args.destination)

    # Pre-process files
    files_to_process = scan_for_files(args.evidence)

    #
    # Start of Plugin Processing
    #
    # plugins to process the file listing
    import plugins.android_browser
    import plugins.android_contacts
    import plugins.android_telephony

    # run plugins

    # Android Browser Parser
    browser_data = plugins.android_browser.android_browser(files_to_process)
    # Android Contact Parser
    contacts_data = plugins.android_contacts.android_contacts(files_to_process)

    # Android Telephony Parser
    telephony_data_sms, telephony_data_threads = plugins.android_telephony.android_telephony(files_to_process)

    print telephony_data_sms
    print "Threads"
    print telephony_data_threads

    #
    # End of Plugin Processing
    #

    #
    # Start of Writers
    #
    import writers.csv_writer

    # Write Contact Data
    writers.csv_writer.csv_writer(browser_data, os.path.join(args.destination,
                                                             'android_browser.csv'))
    writers.csv_writer.csv_writer(contacts_data, os.path.join(args.destination,
                                                     'android_contacts.csv'))
    writers.csv_writer.csv_writer(telephony_data_sms, os.path.join(args.destination,
                                                              'android_telephony_sms.csv'))
    writers.csv_writer.csv_writer(telephony_data_threads, os.path.join(args.destination,
                                                                  'android_telephony_threads.csv'))