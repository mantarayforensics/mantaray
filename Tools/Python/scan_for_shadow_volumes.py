#!/usr/bin/env python3
#This program runs Joachom Metz's vshadowinfo against each NTFS partition found 
#on a disk image and writes out the results to a text file.
#The goal is to allow the examiner to determine if the disk image contains shadow volumes that
#need to be exploited

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 	2013 dougkoster@hotmail.com                 			 #
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

from easygui import *
from get_case_number import *
from get_output_location import *
from select_file_to_process import *
from parted import *
from mount import *
from mount_ewf import *
from done import *
from unix2dos import *
from remove_dupes_module import *
from mmls import *

import os
from os.path import join
import re
import io
import sys
import string
import subprocess
import datetime

def process_shadow_volumes(value, key, Image_Path, outfile_log, case_number, folder_path):

	vshadowinfo_command = "vshadowinfo -o " + str(key) + " " + Image_Path + ">> " + folder_path + "/Partition_" + str(key) + "/shadow_volume_info.txt"
	print("The vshadow info command is: " + vshadowinfo_command)

	#run command
	subprocess.call([vshadowinfo_command], shell=True)

#### MAIN PROGRAM #####################################################################

#get case number
case_number = get_case_number()

#get output location
folder_path = get_output_location(case_number)

#open log file for output
log_file = folder_path + "/" + case_number + "_logfile.txt"
quoted_log_file = "'" +log_file+"'"
outfile_log = open(log_file, 'wt+')

#select dd image to process
Image_Path = select_file_to_process(outfile_log)

#get the filename
filename_to_process = (os.path.basename(Image_Path))
filename_to_process = filename_to_process[:-1]

#check if Image file is in Encase format
if re.search (".E01", Image_Path):
	#get date
	now = datetime.datetime.now()

	#set mount point
	mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S")
	Image_Path = mount_ewf(Image_Path, outfile_log, mount_point)

#call mmls function
partition_info_dict = mmls(outfile, Image_Path)
partition_info_dict_temp = partition_info_dict

#get filesize of mmls_output.txt
file_size = os.path.getsize("/tmp/mmls_output.txt")

#if filesize of mmls output is 0 then run parted
if(file_size == 0):
	print("mmls output was empty, running parted")
	outfile.write("mmls output was empty, running parted")
	#call parted function
	partition_info_dict = parted(outfile, Image_Path)
	#folder_process = select_folder_to_process(outfile)	

else:

	#read through the mmls output and look for GUID Partition Tables (used on MACS)
	mmls_output_file = open("/tmp/mmls_output.txt", 'r')
	for line in mmls_output_file:
		if re.search("GUID Partition Table", line) or re.search("MAC Partition Map", line):
			print("We found a GUID partition table, need to use parted")
			outfile.write("We found a GUID partition table, need to use parted\n")
			#call parted function
			partition_info_dict = parted(outfile, Image_Path)

	#close file
	mmls_output_file.close()

#loop through dictionary containing partition info (filesystem-> VALUE, offset-> KEY)

for key,value in partition_info_dict.items():
	if(value == "ntfs"):
		if not os.path.exists(folder_path + "/Partition_" + str(key)):
			os.makedirs(folder_path + "/Partition_" + str(key))
			print("Just created output folder: " + folder_path + "/Partition_" + str(key))
			outfile_log.write("Just created output folder: " + folder_path + "/Partition_" + str(key) + "\n\n")
		else:
			print("Output folder: " + folder_path + "/Partition_" + str(key))
			
		#call function to process shadow volume info
		process_shadow_volumes(value, key, Image_Path, outfile_log, case_number, folder_path)
	else:
		print("This partition is not formatted NTFS")
		outfile_log.write("This partition is not formatted NTFS\n\n")

outfile_log.close()

#chdir to output_folder
os.chdir(folder_path)

#run text files through unix2dos
for root, dirs, files in os.walk(folder_path):
	for filenames in files:
		#get file extension
		fileName, fileExtension = os.path.splitext(filenames)
		if(fileExtension.lower() == ".txt"):
			full_path = os.path.join(root, filenames)
			quoted_full_path = "'"+full_path+"'"

			print("Running unix2dos against file: " + filenames)
			unix2dos_command = "sudo unix2dos " + filenames
			subprocess.call([unix2dos_command], shell=True)

#unmount and remove mount points
if re.search(".E01", Image_Path):
	if(os.path.exists(mount_point+"_ewf")):
		subprocess.call(['sudo unmount -f ' + mount_point + "_ewf"], shell=True)
		os.rmdir(mount_point + "_ewf")

#tell user the process is done
done(folder_path)
