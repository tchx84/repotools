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

root="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
path=$root/etc/repos.json
name=$1
env=$2

if [ -z $name ]; then
    echo "No repository was given."
    echo "Usage:" $0 "<name> <environment>"
    exit -1
fi

if [ -z $env ]; then
    echo "No environment was given."
    echo "Usage:" $0 "<name> <environment>"
    exit -1
fi


repos="$(${root}/helpers/get_paths.py -p ${path} -e ${env} -n ${name})";

for repo in $repos;
do
    echo "Updating" $repo

    # copy latest packages to updates, if needed
    if [ $env == "updates" ]; then
        $root/helpers/update.py -p $path -n ${name}
        if [ $? != 0 ]; then
            echo "No packages were updated."
            exit -1
        fi
    fi

    # sign packages
    rpm --resign $repo/* &> /dev/null
    if [ $? = 1 ]; then
        echo "Could not sign packages."
        exit -1
    fi

    # update repository metadata
    createrepo --database $repo &> /dev/null
    if [ $? != 0  ]; then
        echo "Could not update repodata."
        exit -1
    fi

done
