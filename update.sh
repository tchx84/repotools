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

env=$1
if [ -z $env ]; then
    echo "No environment was given {testing, updates}."
    exit -1
fi

path=./etc/repos.json
if [ $env == "updates" ]; then
    echo "Updates packages to updates."
    ./repositories.py -p $path

    if [ $? != 0 ]; then
        echo "No packages were updated."
        exit -1
    fi

fi

repos="$(./helpers/find_paths.py -p ${path} -e ${env})";

for repo in $repos;
do
    echo 'Updating ' $repo

    rpm --resign $repo/* &> /dev/null
    if [ $? = 1 ]; then
        echo 'Could not sign packages.'
        exit -1
    fi

    createrepo --database $repo &> /dev/null
    if [ $? != 0  ]; then
        echo "Could not update repodata."
        exit -1
    fi

done
