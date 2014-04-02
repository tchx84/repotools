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


def _get_header(path):
    """ extracts header from package """
    transaction = rpm.ts()
    descriptor = os.open(path, os.O_RDONLY)
    header = transaction.hdrFromFdno(descriptor)
    os.close(descriptor)
    return header


def _get_data(path):
    """ obtains a sub-set of package metadata """
    header = _get_header(path)
    name = header[rpm.RPMTAG_NAME]
    version = '%s-%s' % (header[rpm.RPMTAG_VERSION],
                         header[rpm.RPMTAG_RELEASE])

    if header[rpm.RPMTAG_SOURCE]:
        arch = 'src'
    else:
        arch = header[rpm.RPMTAG_ARCH]

    return name, version, arch


def _get_latest(directory):
    """ classifies latest packages per arch """
    latest = {}

    for path, subdirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.rpm'):
                filepath = os.path.join(path, filename)
                name, version, arch = _get_data(filepath)

                if arch not in latest:
                    latest[arch] = {}

                if name not in latest[arch] or \
                   latest[arch][name]['version'] < version:
                    latest[arch][name] = {'path': filepath,
                                          'version': version}

    return latest


if __name__ == '__main__':
    parser = ArgumentParser(description='latest packages from a directory')
    parser.add_argument('-d', '--dir', type=str, dest='dir', default='.')
    parser.add_argument('-a', '--arch', type=str, dest='arch', default=None)
    args = parser.parse_args()

    latest = _get_latest(args.dir)
    for arch in latest.keys():
        if args.arch is None or args.arch == arch:
            for package in latest[arch].keys():
                print latest[arch][package]['path']
