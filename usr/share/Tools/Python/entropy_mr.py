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
import codecs
from os.path import join
import re
import io
import sys
import string
import subprocess
import pickle
import datetime
import base64

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
from calculate_md5 import *


### process_folder #######################################################################################

def process_folder (folder_to_process, export_file, outfile):
    for root, dirs, files in os.walk (folder_to_process):
        for file_name in files:
            abs_file_path = os.path.join (root, file_name)
            quoted_abs_file_path = '"' + abs_file_path + '"'

            file_name_print = file_name.encode ('utf-8')
            abs_file_path_print = abs_file_path.encode ('utf-8')

            #clean up printable variables
            file_name_print = re.sub ('b\'', '', str (file_name_print))
            file_name_print = re.sub ("'", '', file_name_print)

            abs_file_path_print = re.sub ('b\'', '', str (abs_file_path_print))
            abs_file_path_print = re.sub ("'", '', abs_file_path_print)

            #don't process link files
            if not (os.path.islink (abs_file_path)):

                #get file size
                try:
                    file_size = os.path.getsize (abs_file_path)
                except:
                    print ("Could not get filesize for file: " + abs_file_path)
                    outfile.write ("Could not get filesize for file: " + abs_file_path + "\n")
                if (file_size):
                    try:
                        ent = calc_entropy (abs_file_path)
                        print ("Filename: " + file_name + "\t" + "Entropy: " + ent)

                        export_file.write (ent + "," + str (file_name_print) + "," + str (file_size) + "," + str (
                            abs_file_path_print) + "\n")

                    except:
                        print ("Could not get entropy for file: " + abs_file_path)
                        outfile.write ("Could not get entropy for file: " + str (abs_file_path_print) + "\n")
                else:
                    print ("File: " + file_name + " has 0 file size....skipping")
                    outfile.write ("File: " + file_name + "has 0 file size....skipping\n")
            else:
                print ("File: " + file_name + " is link file....skipping")
                outfile.write ("File: " + file_name + "is link file....skipping\n")


##########################################################################################################

### calc_entropy #########################################################################################

def calc_entropy (file_to_process):
    if (re.search ("'", file_to_process)):
        entropy = subprocess.check_output (
            ['ent ' + '"' + file_to_process + '"' + " | grep Entropy | awk '{print $3}'"], shell=True)
    else:
        entropy = subprocess.check_output (
            ['ent ' + "'" + file_to_process + "'" + " | grep Entropy | awk '{print $3}'"], shell=True)
    entropy = entropy.strip ()
    entropy_string = entropy.decode (encoding='UTF-8')
    return entropy_string


##########################################################################################################


def entropy_mr (item_to_process, case_number, root_folder_path, evidence):
    print ("The item to process is: " + item_to_process)
    print ("The case_name is: " + case_number)
    print ("The output folder is: " + root_folder_path)
    print ("The evidence to process is: " + evidence)

    evidence_no_quotes = evidence
    evidence = '"' + evidence + '"'

    #get datetime
    now = datetime.datetime.now ()

    #set Mount Point
    mount_point = "/mnt/" + "MantaRay_" + now.strftime ("%Y-%m-%d_%H_%M_%S_%f")

    #create output folder path
    folder_path = root_folder_path + "/" + "Entropy"
    check_for_folder (folder_path, "NONE")


    #open a log file for output
    log_file = folder_path + "/Entropy_logfile.txt"
    outfile = open (log_file, 'wt+')

    #open file to write output
    exp_file = folder_path + "/" + case_number + "_entropy.csv"
    export_file = open (exp_file, 'a+', encoding='latin-1', errors="ignore")
    #export_file = open(exp_file, 'a')

    if (item_to_process == "Single File"):
        ent = calc_entropy (evidence)
        print (ent)

    elif (item_to_process == "Directory"):
        folder_to_process = evidence_no_quotes
        process_folder (folder_to_process, export_file, outfile)
    elif (item_to_process == "EnCase Logical Evidence File"):
        file_to_process = evidence
        mount_point = mount_encase_v6_l01 (case_number, file_to_process, outfile)
        process_folder (mount_point, export_file, outfile)

        #umount
        if (os.path.exists (mount_point)):
            subprocess.call (['sudo umount -f ' + mount_point], shell=True)
            os.rmdir (mount_point)
    elif (item_to_process == "Bit-Stream Image"):
        Image_Path = evidence
        #process every file on every partition
        #get datetime
        now = datetime.datetime.now ()

        #set Mount Point
        mount_point = "/mnt/" + now.strftime ("%Y-%m-%d_%H_%M_%S_%f")

        #check if Image file is in Encase format
        if re.search (".E01", Image_Path):

            #strip out single quotes from the quoted path
            #no_quotes_path = Image_Path.replace("'","")
            #print("THe no quotes path is: " +  no_quotes_path)
            #call mount_ewf function
            Image_Path = mount_ewf (Image_Path, outfile, mount_point)


        #call mmls function
        partition_info_dict, temp_time = mmls (outfile, Image_Path)
        partition_info_dict_temp = partition_info_dict

        #get filesize of mmls_output.txt
        file_size = os.path.getsize ("/tmp/mmls_output_" + temp_time + ".txt")


        #if filesize of mmls output is 0 then run parted
        if (file_size == 0):
            print ("mmls output was empty, running parted")
            outfile.write ("mmls output was empty, running parted")
            #call parted function
            partition_info_dict, temp_time = parted (outfile, Image_Path)

        else:

            #read through the mmls output and look for GUID Partition Tables (used on MACS)
            mmls_output_file = open ("/tmp/mmls_output_" + temp_time + ".txt", 'r')
            for line in mmls_output_file:
                if re.search ("GUID Partition Table", line):
                    print ("We found a GUID partition table, need to use parted")
                    outfile.write ("We found a GUID partition table, need to use parted\n")
                    #call parted function
                    partition_info_dict, temp_time = parted (outfile, Image_Path)
            mmls_output_file.close ()


        #loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
        for key, value in sorted (partition_info_dict.items ()):

            #disable auto-mount in nautilis - this stops a nautilis window from popping up everytime the mount
            # command is executed
            cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set " \
                        "org.gnome.desktop.media-handling automount-open false"
            try:
                subprocess.call ([cmd_false], shell=True)
            except:
                print ("Autmount false failed")

            #call mount sub-routine
            success_code, loopback_device_mount = mount (value, str (key), Image_Path, outfile, mount_point)

            if (success_code):
                print ("Could not mount partition with filesystem: " + value + " at offset:" + str (key))
                outfile.write ("Could not mount partition with filesystem: " + value + " at offset:" + str (key))
            else:

                print ("We just mounted filesystem: " + value + " at offset:" + str (key) + "\n")
                outfile.write ("We just mounted filesystem: " + value + " at offset:" + str (key) + "\n")

                #call entropy function for each mount_point
                process_folder (mount_point, export_file, outfile)
                print ("We just finished calculating the entropy for every file...sorting output")

                #unmount and remove mount points
                if (os.path.exists (mount_point)):
                    subprocess.call (['sudo umount -f ' + mount_point], shell=True)
                    os.rmdir (mount_point)
                #unmount loopback device if this image was HFS+ - need to run losetup -d <loop_device> before unmounting
                if not (loopback_device_mount == "NONE"):
                    losetup_d_command = "losetup -d " + loopback_device_mount
                    subprocess.call ([losetup_d_command], shell=True)



        #delete /tmp files created for each partition
        if (os.path.exists ("/tmp/mmls_output_" + temp_time + ".txt")):
            os.remove ("/tmp/mmls_output_" + temp_time + ".txt")



    #close output file
    export_file.close ()

    #sort output file
    sort_command = "strings -a  " + "'" + exp_file + "'" + " |sort -t\| -r -k 2n > " + "'" + folder_path + "'" + "/" + case_number + "_entropy_sorted.csv"
    subprocess.call ([sort_command], shell=True)

    #write header row to export_file
    #sed_command = "sed -i '1i\ Entropy,File Name,File Size,MD5,File Path' " + "'" + folder_path + "'" + "/" + 	case_number +"_entropy_sorted.csv"
    sed_command = "sed -i '1i\ Entropy,File Name,File Size,FilePath' " + "'" + folder_path + "'" + "/" + case_number + "_entropy_sorted.csv"
    subprocess.call ([sed_command], shell=True)

    #remove original output file
    os.remove (exp_file)

    #remove mount points created for this program
    if (os.path.exists (mount_point)):
        os.rmdir (mount_point)
    if (os.path.exists (mount_point + "_ewf")):
        subprocess.call (['sudo umount -f ' + mount_point + "_ewf"], shell=True)
        os.rmdir (mount_point + "_ewf")

