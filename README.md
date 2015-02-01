# AnParser

This project is designed to allow users to parse data from an Android Acquisition in an easy to examine manner

If you are looking to create an Android Acquisition from a physical or virtual device see
https://github.com/chapinb/foroboto for an automated script.

Travis-CI Status: [![Build Status](https://travis-ci.org/anparser/anparser.svg?branch=0.01a)](https://travis-ci.org/chapinb/anparser)

## Authors

Chapin Bryce @chapinb
Preston Miller @pmiller91

## Usage

### Dependencies

* Python 2.7
* Pandas 0.15.2
* Sleuthkit (http://sourceforge.net/projects/sleuthkit/files/sleuthkit/4.1.3/ )
* Pytsk3
* LibEWF

**On Windows, Anaconda-2.1.0 was used to install the Pandas Library**
**You may need to update the SQLite DLL as seen in https://github.com/chapinb/anparser/issues/5 **

## Running the framework

From the command line execute:

    python anparser.py /path/to/evidence/ /output/directory/

## Support

Checkout the [Wiki](https://github.com/chapinb/anparser/wiki) for additional information

Currently supported artifacts as of 2015-01-19:

* Android Browser bookmarks
* Android Browser accounts
* Android Browser preferences
* Android Browser user defaults
* Android Calendar
* Android Chrome cookies
* Android Chrome downloads
* Android Chrome history
* Android Contacts
* Android Downloads
* Android Gallery3d files
* Android Gallery3d picasa
* Android Gmail accounts
* Android Media file listing
* Android SMS data
* Android Message threads
* Android Play Store account data
* Android Play Store library
* Android Play Store local apps
* Android Play Store suggestions
* Google Docs accounts
* Google Docs collection
* Google Talk Accounts (Hangouts)
* Facebook Messenger contacts
* Facebook Messenger messages
* Facebook Messenger threads
* Kik contacts
* Kik chat
* Snapchat friends
* Snapchat chat
* Snapchat files

Currently supported output formats:

* CSV using `|` as delimiter for stability
* XLSX

## Roadmap

Please add requests in the issues pane of Github. As of 2015-01-12 the features to be built include:

### Output formats
* [x] XLSX
* [ ] HTML
* [ ] XML

### Plugins
* [x] Android Calendar
* [x] Android Downloads
* [ ] Android Locations
* [x] Android Gmail

### Other
* [ ] Documentation for adding custom plugins
* [ ] Compiled executable for Windows
* [ ] Error Handling
  * [ ] For reading input
  * [ ] For writing output
* [ ] Unit tests
