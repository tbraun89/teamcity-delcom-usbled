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

import os
import ConfigParser


class Config:
    def __init__(self):
        self.config_file = '/etc/teamcity-usbled/default.conf'

    def server_config(self):
        if os.path.isfile(self.config_file):
            config = ConfigParser.RawConfigParser()
            config.read(self.config_file)

            if len(config.sections()) > 0:
                result = []

                for section in config.sections():
                    current_server = {
                        'url': config.get(section, 'url'),
                        'user': config.get(section, 'username'),
                        'pass': config.get(section, 'password')
                    }

                    result.append(current_server)

                return result
            else:
                raise Warning('There are no servers configured: ' + self.config_file)
        else:
            raise IOError('Config file not found: ' + self.config_file)
