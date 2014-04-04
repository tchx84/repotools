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
import rpm

from argparse import ArgumentParser


class Packages(list):

    def __init__(self, directory, architectures, keyword):
        self._directory = directory
        self._architectures = architectures
        self._keyword = keyword

        self._transaction = rpm.ts()
        self._transaction.setVSFlags(rpm._RPMVSF_NOSIGNATURES)

    def _get_header(self, path):
        """ extracts header from package """

        descriptor = os.open(path, os.O_RDONLY)
        header = self._transaction.hdrFromFdno(descriptor)
        os.close(descriptor)

        return header

    def _get_data(self, path):
        """ obtains a sub-set of package metadata """

        header = self._get_header(path)
        name = header[rpm.RPMTAG_NAME]
        version = '%s-%s' % (header[rpm.RPMTAG_VERSION],
                             header[rpm.RPMTAG_RELEASE])

        arch = header[rpm.RPMTAG_ARCH]
        if header[rpm.RPMTAG_SOURCE]:
            arch = 'src'

        return name, version, arch

    def _do_find(self):
        """ find latest versions of packages """

        # use dict for indexing packages
        _index = {}

        for path, subdirs, files in os.walk(self._directory):
            for filename in files:
                if self._keyword is not None and \
                   self._keyword not in filename:
                    continue

                if not filename.endswith('.rpm'):
                    continue

                filepath = os.path.join(path, filename)
                name, version, arch = self._get_data(filepath)

                if self._architectures is not None and \
                   arch not in self._architectures:
                    continue

                if arch not in _index:
                    # create a new index for arch
                    _index[arch] = {}

                package = _index[arch].get(name, None)

                if package is not None:
                    if version > package['version']:
                        self.remove(package)
                    else:
                        continue

                package = {'name': name,
                           'arch': arch,
                           'version': version,
                           'filename': filename,
                           'path': filepath}
                self.append(package)

                _index[arch][name] = package

    def find(self):
        self._do_find()


if __name__ == '__main__':
    parser = ArgumentParser(description='latest packages from a directory')
    parser.add_argument('-d', '--dir',
                        type=str,
                        dest='directory',
                        default='.')
    parser.add_argument('-a', '--archs',
                        type=str,
                        dest='architectures',
                        default=None,
                        nargs='*')
    parser.add_argument('-s', '--search',
                        type=str,
                        dest='keyword',
                        default=None)
    args = parser.parse_args()

    packages = Packages(args.directory, args.architectures, args.keyword)
    packages.find()

    for package in sorted(packages, key=lambda e: e['name']):
        print package['path']
