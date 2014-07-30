#!/usr/bin/env python3
# This program calculates the entropy for a file, folder or disk image
#The user sets a reporting threshold

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

#import modules
import os
from os.path import join
import re
import io
import sys
import string
import subprocess
import pickle
import datetime

from easygui import *
from get_case_number import *
from get_output_location import *
from select_file_to_process import *
from select_folder_to_process import *
from parted import *
from mmls import *
from mount import *
from mount_ewf import *
from get_ntuser_paths import *
from get_usrclass_paths import *
from get_system_paths import *
from done import *
from unix2dos import *
from check_for_folder import *
from mount_encase_v6_l01 import *


### process_folder #######################################################################################

def process_folder (folder_to_process, export_file):
    for root, dirs, files in os.walk (folder_to_process):
        for file_name in files:

            abs_file_path = os.path.join (root, file_name)

            #get file size
            file_size = os.path.getsize (abs_file_path)
            ent = calc_entropy (abs_file_path)
            print ("Filename: " + file_name + "\t" + "Entropy: " + ent)
            export_file.write (ent + "," + file_name + "," + str (file_size) + "," + abs_file_path + "\n")


##########################################################################################################

### calc_entropy #########################################################################################

def calc_entropy (file_to_process):
    entropy = subprocess.check_output (['ent ' + "'" + file_to_process + "'" + " | grep Entropy | awk '{print $3}'"],
                                       shell=True)
    entropy = entropy.strip ()
    entropy_string = entropy.decode (encoding='UTF-8')
    return entropy_string


##########################################################################################################

def entropy_module (item_to_process, folder_path, case_number):
    #get datetime
    now = datetime.datetime.now ()

    #open a log file for output
    log_file = folder_path + "/" + case_number + "_logfile.txt"
    outfile = open (log_file, 'a')

    #open file to write output
    exp_file = folder_path + "/" + case_number + "_entropy.csv"
    export_file = open (exp_file, 'a')

    if (item_to_process == "file"):
        file_to_process = select_file_to_process (outfile)
        ent = calc_entropy (file_to_process)
        print (ent)

    elif (item_to_process == "folder"):
        folder_to_process = select_folder_to_process (outfile)
        process_folder (folder_to_process, export_file)
    elif (item_to_process == "L01"):
        file_to_process = select_file_to_process (outfile)
        mount_point = mount_encase_v6_l01 (case_number, file_to_process, outfile)
        process_folder (mount_point, export_file)

        #umount
        if (os.path.exists (mount_point)):
            subprocess.call (['sudo umount -f ' + mount_point], shell=True)
            os.rmdir (mount_point)
    elif (item_to_process == "image"):
        Image_Path = select_file_to_process (outfile)

        #process every file on every partition
        #get datetime
        now = datetime.datetime.now ()

        #set Mount Point
        mount_point = "/mnt/" + now.strftime ("%Y-%m-%d_%H_%M_%S")

        #check if Image file is in Encase format
        if re.search (".E01", Image_Path):

            #strip out single quotes from the quoted path
            #no_quotes_path = Image_Path.replace("'","")
            #print("THe no quotes path is: " +  no_quotes_path)
            #call mount_ewf function
            Image_Path = mount_ewf (Image_Path, outfile, mount_point)


        #call mmls function
        partition_info_dict = mmls (outfile, Image_Path)
        partition_info_dict_temp = partition_info_dict

        #get filesize of mmls_output.txt
        file_size = os.path.getsize ("/tmp/mmls_output.txt")


        #if filesize of mmls output is 0 then run parted
        if (file_size == 0):
            print ("mmls output was empty, running parted")
            outfile.write ("mmls output was empty, running parted")
            #call parted function
            partition_info_dict = parted (outfile, Image_Path)

        else:

            #read through the mmls output and look for GUID Partition Tables (used on MACS)
            mmls_output_file = open ("/tmp/mmls_output.txt", 'r')
            for line in mmls_output_file:
                if re.search ("GUID Partition Table", line):
                    print ("We found a GUID partition table, need to use parted")
                    outfile.write ("We found a GUID partition table, need to use parted\n")
                    #call parted function
                    partition_info_dict = parted (outfile, Image_Path)


        #loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
        for key, value in sorted (partition_info_dict.items ()):

            #call mount sub-routine
            success_code = mount (value, str (key), Image_Path, outfile, mount_point)

            if (success_code):
                print ("Could not mount partition with filesystem: " + value + " at offset:" + str (key))
                outfile.write ("Could not mount partition with filesystem: " + value + " at offset:" + str (key))
            else:

                print ("We just mounted filesystem: " + value + " at offset:" + str (key) + "\n")
                outfile.write ("We just mounted filesystem: " + value + " at offset:" + str (key) + "\n")

                #call entropy function for each mount_point
                process_folder (mount_point, export_file)

                #unmount and remove mount points
                if (os.path.exists (mount_point)):
                    subprocess.call (['sudo umount -f ' + mount_point], shell=True)
                    os.rmdir (mount_point)

    #close output file
    export_file.close ()

    #sort output file
    sort_command = "strings -a  " + "'" + exp_file + "'" + " |sort -t\| -r -k 2n > " + "'" + folder_path + "'" + "/" + case_number + "_entropy_sorted.csv"
    subprocess.call ([sort_command], shell=True)

    #write header row to export_file
    sed_command = "sed -i '1i\ Entropy,File Name,File Size,File Path' " + "'" + folder_path + "'" + "/" + case_number + "_entropy_sorted.csv"
    subprocess.call ([sed_command], shell=True)

    #remove original output file
    os.remove (exp_file)
