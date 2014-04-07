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

if [ $# -lt 2 ]; then
    echo "usage:" $0 "<name>" "<files>"
    exit -1
fi

name=$1
packages="${@:2}"

path=./etc/repos.json
user="$(./helpers/get_key.py -p ${path} -k user)"
server="$(./helpers/get_key.py -p ${path} -k server)"
directory="$(./helpers/get_key.py -p ${path} -k directory)"
remote_path="$(./helpers/get_paths.py -p ${path} -e testing -n ${name})"
packages="$(./helpers/purge.py -p ${path} -n ${name} -f ${packages})"

echo "Uploading to:"
echo -e '\t'$user@$server:$remote_path/

echo "Packages:"
for package in $packages;
do
    echo -e '\t'$(basename $package)
done

echo "Please type \"confirm\" to continue..."
read confirm

if [ "$confirm" != "confirm" ]; then
    echo "Nothing has been done."
    exit -1
fi

scp $packages $user@$server:$remote_path/
