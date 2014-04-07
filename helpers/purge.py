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
# You should have received a copy of the GNU General Public Lic

import os
import sys
import json

from argparse import ArgumentParser

# XXX HORRIBLE :(
_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(_path+"/..")

from libs.packages import Packages


def _purge(path, name, files):
    config = None
    with open(path) as file:
        config = json.loads(file.read())

    repo = None
    for _repo in config['list']:
        if name == _repo['name']:
            repo = _repo
            break

    if repo is None:
        return

    packages = Packages(None, repo['archs'], repo['keyword'])
    for filepath in files:
        filename = os.path.basename(filepath)
        if not packages._match_name(filename):
            continue

        name, version, arch = packages._get_data(filepath)
        if not packages._match_arch(arch):
            continue

        print filepath


def _main():
    parser = ArgumentParser(description='')
    parser.add_argument('-p',
                        '--path',
                        type=str,
                        dest='path',
                        required=True)
    parser.add_argument('-n',
                        '--name',
                        type=str,
                        dest='name',
                        required=True)
    parser.add_argument('-f',
                        '--files',
                        type=str,
                        dest='files',
                        nargs='*',
                        required=True)

    args = parser.parse_args()
    _purge(args.path, args.name, args.files)


if __name__ == '__main__':
    _main()
