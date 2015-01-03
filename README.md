# AnParser

This project is designed to allow users to parse data from an Android Acquisition in an easy to examine manner

If you are looking to create an Android Acquisition from a physical or virtual device see
https://github.com/chapinb/foroboto for an automated script.

## Usage

### Dependencies

* Python 2.7

From the command line execute:

    python anparser.py /path/to/evidence/ /output/directory/

## Support

Currently supported artifacts:

* Android Contacts Database
* Android SMS Contact Database

Currently supported output formats:

* CSV using `|` as delimiter for stability


## Roadmap

Please add requests in the issues pane of Github. As of 2015-01-02 the features to be built include:

### Output formats
* XLSX
* HTML
* XML

### Plugins
* Android Calendar
* Android Downloads
* Android Locations
* Android Gmail

### Other
* Documentation for adding custom plugins
* Compiled executable for Windows
* Error Handling
  * For reading input
  * For writing output
* Unit tests