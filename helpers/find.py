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

from argparse import ArgumentParser

from libs.packages import Packages


def find(directory, architectures, keywords):
    packages = Packages(architectures, keywords)
    packages.find(directory)

    for package in sorted(packages, key=lambda e: e['name']):
        print package['path']


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
                        dest='keywords',
                        nargs='*',
                        default=None)

    args = parser.parse_args()
    find(args.directory, args.architectures, args.keywords)
