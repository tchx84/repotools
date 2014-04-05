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

RPM_MACROS_PATH=~/.rpmmacros

gpg --batch --gen-key signing.batch
gpg --import key.private
gpg --list-secret-keys

gpg --export -a 'One Education' > signing.keys
sudo rpm --import signing.keys

echo "%_signature gpg" > $RPM_MACROS_PATH
echo "%_gpg_name One Education (One Laptop Per Child Australia) <info@one-education.org>" >> $RPM_MACROS_PATH
