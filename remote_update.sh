#!/bin/bash -

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

name=$1
env=$2
keywords="${@:3}"

path=./etc/repos.json
user="$(./helpers/get_key.py -p ${path} -k user)"
server="$(./helpers/get_key.py -p ${path} -k server)"
directory="$(./helpers/get_key.py -p ${path} -k directory)"

ssh $user@$server $directory/update.sh $name $env $keywords
