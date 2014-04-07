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


class Packages(list):

    def __init__(self, architectures, keywords):
        self._architectures = architectures
        self._keywords = keywords

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

    def _match_keyword(self, filename):
        """ check if filename matches accepted keywords """

        if not filename.endswith('.rpm'):
            return False

        # act like OR
        if self._keywords:
            for keyword in self._keywords:
                if keyword in filename:
                    return True
            return False

        return True

    def _match_arch(self, arch):
        """ check if arch matches accepted archs """

        if self._architectures is not None and \
           arch not in self._architectures:
            return False

        return True

    def find(self, directory):
        """ find latest versions of packages """

        # use dict for indexing packages
        _index = {}

        for path, subdirs, files in os.walk(directory):
            for filename in files:
                if not self._match_keyword(filename):
                    continue

                filepath = os.path.join(path, filename)
                name, version, arch = self._get_data(filepath)

                if not self._match_arch(arch):
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

    def purge(self, files):
        """ purge packages from list of files """

        for path in files:
            filename = os.path.basename(path)
            if not self._match_keyword(filename):
                continue

            name, version, arch = self._get_data(path)
            if not self._match_arch(arch):
                continue

            package = {'name': name,
                       'arch': arch,
                       'version': version,
                       'filename': filename,
                       'path': path}
            self.append(package)
