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

import logging
import logging.handlers
import time
import sys
import os
import errno
from daemon import runner
import config
import ConfigParser
import teamcity_api
from led_controller import set_status


class TeamcityUsbLed:
    def __init__(self, logger):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/var/run/teamcity-delcom-usbled.pid'
        self.pidfile_timeout = 5
        self.logger = logger

    def run(self):
        self.logger.info('Starting TeamCity USB Led')

        try:
            conf = config.Config().server_config()
        except Warning as e:
            self.logger.warning(str(e))
            self.logger.critical('Exiting: ' + os.strerror(int(errno.EINVAL)))
            sys.exit(errno.EINVAL)
        except IOError as e:
            self.logger.error(str(e))
            self.logger.critical('Exiting: ' + os.strerror(int(errno.EINVAL)))
            sys.exit(errno.EINVAL)
        except ConfigParser.NoOptionError as e:
            self.logger.error(str(e))
            self.logger.critical('Exiting: ' + os.strerror(int(errno.EINVAL)))
            sys.exit(errno.EINVAL)
        except Exception as e:
            self.logger.critical(str(e))
            self.logger.critical('Exiting: ' + os.strerror(-1))
            sys.exit(-1)

        api_list = []
        for server in conf:
            try:
                api_list.append(teamcity_api.TeamCityAPI(server['url'], server['user'], server['pass']))
            except Exception:
                self.logger.error('Can not connect to: ' + server['url'])
                set_status(0)
                self.logger.critical('Exiting: ' + os.strerror(int(errno.ECONNABORTED)))
                sys.exit(errno.ECONNABORTED)

        while True:
            status = 0

            for api in api_list:
                try:
                    if api.failing_count() > 0:
                        status = -1
                        break
                except Exception as e:
                    status = 0
                    self.logger.error(str(e))
                    break

                status = 1

            set_status(status)

            time.sleep(30)


def main():
    logger = logging.getLogger('TeamcityUsbLedLog')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.handlers.RotatingFileHandler('/var/log/teamcity-delcom-usbled/info.log',
                                                   maxBytes=524288, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    app = TeamcityUsbLed(logger)

    daemon = runner.DaemonRunner(app)
    daemon.daemon_context.files_preserve = [handler.stream]
    daemon.do_action()
