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

import json

from argparse import ArgumentParser


def get_key(path, key):
    with open(path) as file:
        config = json.loads(file.read())
        print config[key]


if __name__ == '__main__':
    parser = ArgumentParser(description='get repository key')
    parser.add_argument('-p', '--path', type=str, dest='path', required=True)
    parser.add_argument('-k', '--key', type=str, dest='key', required=True)

    args = parser.parse_args()
    get_key(args.path, args.key)
