__author__ = 'cbryce'
__license__ = 'GPLv3'
__date__ = '01/26/2014'
__version__ = '0.01'

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

import os

class BootstrapHTML():

    def __init__(self, outfile=None):
        self.outfile = outfile
        self.outfile = self.open_outfile()
        self.title = None
        self.header = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="html_support/bootstrap.min.css">
<script src="html_support/jquery.min.js"></script>
<script src="html_support/bootstrap.min.js"></script>
</head>
        """

        self.jumbo = """<div class="container">
    <div class="jumbotron">
        <h1>AnParser Overview</h1>

        <small>Overview of artifacts from AnParser Results of [Insert Path here]</small>
    </div>"""

        # Write Jumbo Header
        self.write(self.jumbo)

    def open_outfile(self):
        return open(self.outfile, 'w')

    def close_outfile(self):

        # Write Footer
        self.write("""
                    </div>
                    </body>
                    </head>
                    </html>
                    """)

        try:
            self.outfile.close()
        except IOError:
            IOError('Unable to write to output file')

    def write(self, information):
        self.outfile.write(information)


    def setup_account_information(self):
        setup = """
            <h2>Account Information:</h2>
            <div class="row">"""
        self.write(setup)

    def add_account_information(self, information):

        for info in information:
            try:
                account_type = info[0]
                account_value = info[1]
                data = """
                        <div class="col-sm-4">
                            <p>""" + account_type + """</p>
                        </div>
                        <div class="col-sm-8">
                            <p>""" + account_value + """</p>
                        </div>
                        """

            except:
                data = ''
                pass

            self.write(data)

