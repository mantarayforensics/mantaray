#!/usr/bin/env python3
# This program will recursively remove the duplicates from a folder and all subfolders using fdupes
#INPUT: Absolute path to the folder you want to process
#OUTPUT: None
#NOTE: FDUPES must be installed for this program to work properly

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2011 					                 #
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

import os
from os.path import join
import re
import shutil
import io
import sys
import string
import subprocess

from easygui import *
from get_output_location import *
from done import *
from unix2dos import *
from check_for_folder import *


def remove_duplicates_mr (root_folder_path, evidence):
    print ("The output folder is: " + root_folder_path)
    print ("The evidence to process is: " + evidence)

    evidence = '"' + evidence + '"'

    #get datetime
    now = datetime.datetime.now ()

    #create output folder path
    folder_path = root_folder_path + "/" + "Remove_Duplicates"
    check_for_folder (folder_path, "NONE")

    remove_dupes_command = "sudo fdupes -r -d -N " + evidence + " > " + '"' + folder_path + \
                           "/fdupes_duplicates_log.txt" + '"'
    print ("The remove dupes command is: " + remove_dupes_command + "\n\n")
    print ("Removing duplicate files recursively from folder: " + evidence + "\n\n")

    #run the remove dupes command
    subprocess.call ([remove_dupes_command], shell=True)

    #get filesize of mmls_output.txt
    file_size = os.path.getsize (folder_path + "/fdupes_duplicates_log.txt")

    #if filesize of mmls output is 0 then run parted
    if (file_size == 0):
        print ("No duplicates found\n")
        outfile = open (folder_path + "/fdupes_duplicates_log.txt", 'wt+')
        outfile.write ("No duplicate files found!")
        #close outfile
        outfile.close ()
    else:
        #if log file exists then run unix2dos against the logfile
        unix2dos (folder_path + "/fdupes_duplicates_log.txt")

    #remove empty directories
    for root, dirs, files in os.walk (root_folder_path):
        for directories in dirs:
            dir_name = os.path.join (root, directories)
            #if directory is empty then delete it
            if not os.listdir (dir_name):
                os.rmdir (dir_name)

