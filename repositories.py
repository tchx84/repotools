#!/usr/bin/env python

# Copyright (c) 2014 Martin Abente Lahaye. - tch@sugarlabs.org
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software

import os
import json
import shutil

from packages import Packages


class Repositories(object):

    REPOS_PATH = 'repos.json'
    CONFIRM_TEXT = 'confirm'

    def __init__(self):
        self._repos = self._load_repos()

    def _load_repos(self):
        """ load repositories confis form file """

        if not os.path.exists(self.REPOS_PATH):
            print '%s not found' % self.REPOS_PATH
            raise ValueError

        with open(self.REPOS_PATH) as file:
            return json.loads(file.read())

    def _retrieve_repos(self):
        """ extracts and purge packages """

        for repo in self._repos['list']:
            packages = Packages(repo['testing'],
                                repo['archs'],
                                repo['keyword'])
            packages.find()

            def _purged(path, name):
                return not os.path.exists(os.path.join(path, name))

            # XXX at this point packages is not longer Packages class
            packages = [p for p in packages
                        if _purged(repo['updates'], p['filename'])]

            # add purged packages list
            repo['packages'] = packages

    def _confirmed(self):
        """ display interactive confirmation """

        for repo in self._repos['list']:
            if not repo['packages']:
                continue

            print 'update %s' % repo['name']
            for package in sorted(repo['packages'], key=lambda e: e['name']):
                print '\t%s' % package['filename']

        print 'Please type \"%s\" to continue...' % self.CONFIRM_TEXT
        check = raw_input(':')

        return check == self.CONFIRM_TEXT

    def _do_update(self):
        """ copy updated testing to updates """

        for repo in self._repos['list']:
            if not repo['packages']:
                continue

            for package in sorted(repo['packages'], key=lambda e: e['name']):
                path = os.path.join(repo['updates'], package['filename'])
                shutil.copyfile(package['path'], path)
                print 'copying %s to %s' % (package['filename'], repo['name'])
                print '\tfrom %s \n\tto %s' % (package['path'], path)

    def update(self):
        self._retrieve_repos()
        if self._confirmed():
            self._do_update()
        else:
            print 'Nothing has been done'


def _main():
    repos = Repositories()
    repos.update()

if __name__ == '__main__':
    _main()
