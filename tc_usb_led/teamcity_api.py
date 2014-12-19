# TeamCity Delcom USB Led Daemon
# Copyright (C) 2014  Torsten Braun
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ETree


class TeamCityAPI:
    def __init__(self, server, username, password):
        self.server = server
        response = requests.get(server + 'httpAuth/app/rest/server', auth=HTTPBasicAuth(username, password))
        self.cookies = response.cookies

    def failing_count(self):
        response = requests.get(self.server + 'app/rest/builds/?locator=status:failure,sinceBuild:(status:success)',
                                cookies=self.cookies)
        tree = ETree.fromstring(response.text)

        return int(tree.attrib['count'])
