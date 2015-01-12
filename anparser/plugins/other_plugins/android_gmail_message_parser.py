__author__ = 'cbryce'
__license__ = ''
__date__ = ''
__version__ = ''

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
import android_gmail_message_extractor


def android_gmail_message_parser(file_listing, output_dir):

    filesToProcess = []
    account_info = dict()

    for fileEntry in file_listing:
        if os.path.basename(fileEntry).startswith('mailstore.') and fileEntry.endswith('.db') and \
                fileEntry.__contains__(
                '@'):
            accountNameInternal = fileEntry.split('mailstore.', 1)[1]
            accountNameInternal = accountNameInternal.split('.db')[0]

            account_info['account'] = accountNameInternal
            account_info['path'] = fileEntry

            filesToProcess.append(account_info)
            account_info = dict()

    for fileEntry in filesToProcess:
        accountOutputPath = os.path.join(output_dir, fileEntry['account'].split('@', 1)[0])
        if not os.path.exists(accountOutputPath):
            os.makedirs(accountOutputPath)
        android_gmail_message_extractor.main(fileEntry['path'], accountOutputPath)
