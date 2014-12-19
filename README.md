TeamCity Delcom 807241 USB Led
======================

This is a small Python tool to display the status of one or more
TeamCity servers on a **Delcom 807241 USB Led**.

Requirements
----------------------

* Python 2.7.x
* Python `daemon` library
* Python `requests` library
* The `delcome-usbled` tool ([https://github.com/tbraun89/delcom-usbled](https://github.com/tbraun89/delcom-usbled))

Installation
----------------------

* Clone the Git Repository
* Run `sudo python setup.py install`
* Add your servers to `/etc/teamcity-usbled/default.conf`
* Start the service with `sudo service teamcity-usbled start`

The script automatically adds an init script so the service
can start up each reboot.

Configuration
----------------------

The configuration is a INI styled file, you each server has
a section with `url`, `username` and `password`. Only the
root user has read and write access to the configuration
file.