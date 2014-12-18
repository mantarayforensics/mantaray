#This program will recursively remove the duplicates from a folder and all subfolders using fdupes
#INPUT: Absolute path to the folder you want to process
#OUTPUT: None
#NOTE: FDUPES must be installed for this program to function properly

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2011                 					                 #
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

#import modules
import os
import subprocess


def remove_dupes_module_noask(folder, outfile, partition_offset):

    #add quotes to image path in case of spaces
    quoted_path = "'" +folder +"'"

    no_quotes = quoted_path.replace("'","")

    remove_dupes_command = "sudo fdupes -r -d -N " + quoted_path + " > " + "/tmp/fdupes_duplicates_log.txt"
    print("The remove dupes command is: " + remove_dupes_command + "\n\n")
    outfile.write("The remove dupes command is: " + remove_dupes_command + "\n\n")
    print ("Removing duplicate files recursively from folder: " + quoted_path + "\n\n")

    #run the remove dupes command
    subprocess.call([remove_dupes_command], shell=True, stderr=subprocess.STDOUT)

    #get filesize of mmls_output.txt
    file_size = os.path.getsize("/tmp/fdupes_duplicates_log.txt")

    #if filesize of mmls output is 0 then run parted
    if(file_size == 0):
        print("No duplicates found\n")
        outfile = open("/tmp/fdupes_duplicates_log.txt", 'wt')
        outfile.write("No duplicate files found!")
        #close outfile
        outfile.close()

    #remove empty directories
    for root,dirs,files in os.walk(no_quotes):
        for directories in dirs:
            dir_name = os.path.join(root,directories)
            #if directory is empty then delete it
            if not os.listdir(dir_name):
                os.rmdir(dir_name)