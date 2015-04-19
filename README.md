# AnParser

This project is designed to allow users to parse data from an Android Acquisition in an easy to examine manner

If you are looking to create an Android Acquisition from a physical or virtual device see
https://github.com/chapinb/foroboto for an automated script.

Travis-CI Status: [![Build Status](https://travis-ci.org/anparser/anparser.svg?branch=0.01a)](https://travis-ci.org/anparser/anparser)

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

Currently supported artifacts as of 2015-02-12:

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
* Android Emergencymode
* Android Gallery3d files
* Android Gallery3d picasa
* Android Logsprovider SMS logs
* Android Gmail accounts
* Android Media file listing
* Android SMS data
* Android Message threads
* Android Play Store account data
* Android Play Store library
* Android Play Store local apps
* Android Play Store suggestions
* Facebook Messenger contacts
* Facebook Messenger messages
* Facebook Messenger threads
* Google Docs accounts
* Google Docs collection
* Google Talk Accounts (Hangouts)
* Infraware Polaris contacts
* Infraware Polaris files & shared files
* Infraware Polaris messages
* Kik contacts
* Kik chat
* Samsung GalaxyFinder contents
* Samsung GalaxyFinder geotags
* Skype users
* Skype documents
* Skype conversations & calls
* Snapchat friends
* Snapchat chat
* Snapchat files
* TeslacoilSW all apps
* TeslacoilSW favorites
* Valve debug
* Valve friends
* Valve messages
* Venmo comments
* Venmo friends
* Venmo stories (transactions)
* Vlingo contacts

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
* [x] Android Browser
* [x] Android Calendar
* [x] Android Chrome
* [x] Android Contacts
* [x] Android Downloads
* [x] Android EmergencyMode
* [x] Android Gallery3d
* [x] Android Gmail
* [ ] Android Locations
* [x] Android Logsprovider
* [x] Android Media
* [x] Android MMS
* [x] Android Telephony
* [x] Android Vending
* [x] Facebook Katana
* [x] Facebook Orca
* [x] Google Docs
* [x] Google Plus
* [x] Infraware Office (Polaris)
* [x] Kik
* [x] Samsung Galaxyfinder
* [x] Skype
* [x] Snapchat
* [x] TeslacoilSW
* [x] Valve Steam
* [x] Venmo
* [x] Vlingo

### Other
* [ ] Documentation for adding custom plugins
* [ ] Compiled executable for Windows
* [ ] Error Handling
  * [ ] For reading input
  * [ ] For writing output
* [ ] Unit tests
