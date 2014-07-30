# RUN MMLS against Disk Image
#INPUT - absolute path to logfile, absolute path to Image File
#OUTPUT - returns a dictionary containing the offset (key) and filesystem (value) of every partition found on the drive

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

import re
import io
import sys
import string
import subprocess
import datetime


def mmls (outfile, Image_Path):
    #initiate variables
    partition_table = "NONE"
    partition_info_dict = {}
    #get datetime
    now = datetime.datetime.now ()

    #get time for temp file to make it unique
    temp_time = now.strftime ("%Y-%m-%d_%H_%M_%S_%f")

    #set up mmls command
    mmls_command = "mmls -i raw " + Image_Path + " > /tmp/mmls_output_" + temp_time + ".txt"
    outfile.write ("The mmls command is: " + mmls_command + "\n")

    #run mmls and collect output in tmp folder
    subprocess.call ([mmls_command], shell=True)

    #open mmls output
    infile = open ('/tmp/mmls_output_' + temp_time + '.txt', 'rt+')

    #print out partition table for review
    for line in infile:
        if (re.search (":0\d", line)):
            print (line)
            outfile.write (line)
    infile.close ()
    #open mmls output
    infile = open ('/tmp/mmls_output_' + temp_time + '.txt', 'rt+')

    for line in infile:
        if (re.search (":0\d", line)):
            #split line on space
            line_split = line.split (' ')

            #get sector offset
            partition_start = line_split[5]
            partition_start = int (partition_start) * 512

            print ("The offset is: " + str (partition_start))

            #figure out the partition type
            if (re.search ("0x27", line)) or (re.search ("0x07", line)) or (re.search ("0x12", line)):
                partition_filesystem = "ntfs"
                print ("The filesystem is: " + partition_filesystem)
                #push sector information and fs onto dictionary
                partition_info_dict[partition_start] = partition_filesystem
            elif (re.search ("0x01", line)) or (re.search ("0x11", line)) or (re.search ("0xde", line)):
                partition_filesystem = "fat"
                print ("The filesystem is: " + partition_filesystem)
                #push sector information and fs onto dictionary
                partition_info_dict[partition_start] = partition_filesystem
            elif (re.search ("DOS FAT 16", line)) or (re.search ("0x0E", line)) or (re.search ("0x1E", line)) or (
            re.search ("0x90", line)) or (re.search ("0x92", line)) or (re.search ("0x9a", line)) or (
            re.search ("0x06", line)):
                partition_filesystem = "fat16"
                print ("The filesystem is: " + partition_filesystem)
                #push sector information and fs onto dictionary
                partition_info_dict[partition_start] = partition_filesystem
            elif (re.search ("Win95 FAT32", line)) or (re.search ("0x8b", line)) or (re.search ("0x8c", line)) or (
            re.search ("0x97", line)) or (re.search ("0x98", line)) or (re.search ("0xcb", line)) or (
            re.search ("0xcc", line)) or (re.search ("0xdd", line)):
                partition_filesystem = "fat32"
                print ("The filesystem is: " + partition_filesystem)
                #push sector information and fs onto dictionary
                partition_info_dict[partition_start] = partition_filesystem
            elif (re.search ("Apple_HFS", line)):
                partition_filesystem = "hfs"
                print ("The filesystem is: " + partition_filesystem)
                #push sector information and fs onto dictionary
                partition_info_dict[partition_start] = partition_filesystem
            elif (re.search ("0x17", line)):
                partition_filesystem = "hpfs"
                print ("The filesystem is: " + partition_filesystem)
                #push sector information and fs onto dictionary
                partition_info_dict[partition_start] = partition_filesystem
            elif (re.search ("0x83", line)):
                partition_filesystem = "ext"
                print ("The filesystem is: " + partition_filesystem)
                #push sector information and fs onto dictionary
                partition_info_dict[partition_start] = partition_filesystem

    return partition_info_dict, temp_time
