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

import sys
import json

from argparse import ArgumentParser


def _read_paths(path, env, name):
    with open(path) as file:
        config = json.loads(file.read())
        for repo in config['list']:
            if name and name != repo['name']:
                continue
            print repo[env]

def _main():
    parser = ArgumentParser(description='find paths by environment')
    parser.add_argument('-p', '--path', type=str, dest='path', required=True)
    parser.add_argument('-e', '--env', type=str, dest='env', required=True)
    parser.add_argument('-n', '--name', type=str, dest='name', default=None)

    args = parser.parse_args()
    _read_paths(args.path, args.env, args.name)


if __name__ == '__main__':
   _main()
