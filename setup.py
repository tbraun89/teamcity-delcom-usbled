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

from distutils.core import setup
from distutils.command.install import install
from subprocess import call
import os
import shutil


class CreateCustomFilesCommand(install):
    def run(self):
        if not os.path.exists('/etc/teamcity-usbled'):
            os.mkdir('/etc/teamcity-usbled')
            shutil.copyfile('bin/init/default.conf', '/etc/teamcity-usbled/default.conf')
            call(['chmod', '600', '/etc/teamcity-usbled/default.conf'])

        if not os.path.exists('/var/log/teamcity-delcom-usbled'):
            os.mkdir('/var/log/teamcity-delcom-usbled')

        shutil.copyfile('bin/init/teamcity-usbled', '/etc/init.d/teamcity-usbled')
        call(['chmod', '755', '/etc/init.d/teamcity-usbled'])
        call(['update-rc.d', 'teamcity-usbled', 'start', '20', '3', '5', '.', 'stop', '20', '0', '1', '2', '6'])
        install.run(self)


setup(
    name='teamcity-delcom-usbled',
    version='1.0.0',
    packages=['tc_usb_led'],
    scripts=['bin/teamcity-usbled'],
    url='',
    license='GPL',
    author='Torsten Braun',
    author_email='tbraun@tnt-web-solutions.de',
    description='TeamCity Delcom USB Led Daemon.',
    requires=['daemon', 'requests'],
    cmdclass={
        'install': CreateCustomFilesCommand
    }
)
