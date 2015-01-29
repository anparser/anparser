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


class OverviewParser():
    """
    Used to parse the input data and extract the useful information to write with HTMLDashboardWriter()
    """

    def __init__(self):
        pass


class HTMLDashboardWriter():
    """
    Writes standard data to an HTML file
    """
    def __init__(self):
        self.header = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <!-- Bootstrap core CSS -->
    <link href="html_support/bootstrap.min.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="html_support/dashboard.css" rel="stylesheet">
  </head>
'''
        self.title = ''
        self.navbar = '''
<nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar"
      aria-expanded="false" aria-controls="navbar">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">AnParser Dashboard</a>
    </div>
    <div id="navbar" class="navbar-collapse collapse">
      <ul class="nav navbar-nav navbar-right">
        <li><a href="#">Dashboard</a></li>
      </ul>
      <form class="navbar-form navbar-right">
        <input type="text" class="form-control" placeholder="Search...">
      </form>
    </div>
  </div>
</nav>
        '''
        self.dashboard_first_section = '''<div class="container-fluid"> <h1 class="page-header">Dashboard</h1>'''
        self.dashboard_section_title = ''
        self.dashboard_section = '<h2 class="sub-header">' + self.dashboard_section2_title + '</h2>'
        self.dashboard_section_table_headers = []
        self.dashboard_section_table_data = []

    def _build_table_headers(self):
        """
        Private class that builds out the needed components for a table header
        :return: string html of table header
        """
        table_writer = '<div class="table-responsive"><table class="table table-striped"><thead><tr>'
        for table_name in self.dashboard_section_table_headers:
            table_writer += '<th>' + table_name + '</th>'

        table_writer += '</tr></thead>'

        return table_writer

    def _build_table_data(self):
        """
        Private class that builds out the table
        :return: string html of table data
        """
        table_writer = '<tbody>'
        for row in self.dashboard_section_table_data:
            table_writer += '<tr>'
            for cell in row:
                table_writer += '<td>' + cell + '</rd>'
            table_writer += '</tr>'

        table_writer += '</tbody></table></div>'

        return table_writer