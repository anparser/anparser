# AnParser

This project is designed to allow users to parse data from an Android Acquisition in an easy to examine manner

If you are looking to create an Android Acquisition from a physical or virtual device see
https://github.com/chapinb/foroboto for an automated script.

## Authors

Chapin Bryce @chapinb
Preston Miller @pmiller91

## Usage

### Dependencies

* Python 2.7

**You may need to update the SQLite DLL as seen in https://github.com/chapinb/anparser/issues/5 **

## Running the framework

From the command line execute:

    python anparser.py /path/to/evidence/ /output/directory/

## Support

Currently supported artifacts as of 2015-01-12:

* Android Contacts Database
* Android SMS Contact Database
* Android Media Database
* Android Browser Database
* Android Browsing XML Preferences
* Android Vending Database (Play Store)
* Android Vending XML Preferences (Play Store)
* Android Downloads Database
* Android Gmail Database
* Android Gmail Message Extraction
* Google Docs Database
* Facebook Messenger (Orca)

Currently supported output formats:

* CSV using `|` as delimiter for stability

## Roadmap

Please add requests in the issues pane of Github. As of 2015-01-12 the features to be built include:

### Output formats
* [ ] XLSX
* [ ] HTML
* [ ] XML

### Plugins
* [ ] Android Calendar
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