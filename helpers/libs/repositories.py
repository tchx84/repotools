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

    CONFIRM_TEXT = 'confirm'

    def __init__(self, path, names, keywords):
        self._path = path
        self._names = names
        self._keywords = keywords
        self._repos = None

        with open(self._path) as file:
            self._repos = json.loads(file.read())

    def _find(self):
        """ extracts and purge packages """

        for repo in self._repos['list']:
            if self._names and \
               repo['name'] not in self._names:
                continue

            keywords = repo['keywords']
            if self._keywords:
                # overwrite repo definition
                keywords = self._keywords

            packages = Packages(repo['archs'], keywords)
            packages.find(repo['testing'])

            def _purged(path, name):
                return not os.path.exists(os.path.join(path, name))

            # XXX at this point packages is not longer Packages class
            packages = [p for p in packages
                        if _purged(repo['updates'], p['filename'])]

            repo['packages'] = packages

    def _confirm(self):
        """ display interactive confirmation """

        empty = True

        for repo in self._repos['list']:
            if 'packages' not in repo or \
               not repo['packages']:
                continue

            empty = False
            print 'update %s' % repo['name']
            for package in sorted(repo['packages'], key=lambda e: e['name']):
                print '\t%s' % package['filename']

        if not empty:
            print 'Please type \"%s\" to continue...' % self.CONFIRM_TEXT
            check = raw_input(':')
            return check == self.CONFIRM_TEXT
        else:
            return False

    def _do_update(self):
        """ copy updated testing to updates """

        for repo in self._repos['list']:
            if 'packages' not in repo or \
               not repo['packages']:
                continue

            for package in sorted(repo['packages'], key=lambda e: e['name']):
                path = os.path.join(repo['updates'], package['filename'])
                print 'copying %s to %s' % (package['filename'], repo['name'])
                print '\tfrom %s \n\tto %s' % (package['path'], path)
                shutil.copyfile(package['path'], path)

    def update(self):
        self._find()
        if self._confirm():
            self._do_update()
            return True
        else:
            return False
