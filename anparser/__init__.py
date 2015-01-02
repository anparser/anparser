__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '20150102'
__version__ = '0.00'

# Imports
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
    files_to_process = scan_for_files(sys.argv[1])

    # plugins to process the file listing
    import plugins.android_contacts

    data = plugins.android_contacts.android_contacts(files_to_process)

    import writers.csv_writer

    writers.csv_writer.csv_writer(data, '../LG_Phone/report0.00.csv')