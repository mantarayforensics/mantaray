#!/usr/bin/env python3
# calculate MD5

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2013 douglas.koster@mantech.com				 #
#This program is free software: you can redistribute it and/or modify    #
#it under the terms of the GNU General Public License as published by    #
#the Free Software Foundation, either version 3 of the License, or       #
#(at your option) any later version.                                     #
#
#This program is distributed in the hope that it will be useful,         #
#but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#GNU General Public License for more details.                            #
#
#You should have received a copy of the GNU General Public License       #
#along with this program.  If not, see http://www.gnu.org/licenses/.     #
#########################COPYRIGHT INFORMATION############################

## TODO REplace with Python Module

import subprocess


def calculate_md5 (abs_file_path):
    print ("About to calculate MD5 for file: " + abs_file_path)
    #get md5 hash for file
    md5 = subprocess.check_output (['md5sum ' + "'" + abs_file_path + "'" + " | awk '{print $1}'"], shell=True,
                                   universal_newlines=True)

    return md5

