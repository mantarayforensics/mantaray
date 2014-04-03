#!/usr/bin/env python3
#This program runs foremost against either a disk image (DD or E01) or a folder.  If it is run
#against a disk image it will carve the unallocated of every partition on the disk image

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 						                 #
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
from remove_dupes_module_noask_mr import *
from mmls import *
from check_for_folder import *

import os
from os.path import join
import re
import io
import sys
import string
import subprocess
import datetime

### MAIN PROGRAM ##########################################################################################################################################


def carve_unallocated_mr(item_to_process, case_number, root_folder_path, evidence, options):
	print("The item to process is: " + item_to_process)
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)
	print("The options selected were: " + options)

	evidence = '"' + evidence + '"'

	#get datetime
	now = datetime.datetime.now()

	#set Mount Point
	mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S")
	
	#create output folder path
	folder_path = root_folder_path + "/" + "Foremost"
	check_for_folder(folder_path, "NONE")
	

	#open a log file for output
	log_file = folder_path + "/Foremost_logfile.txt"
	outfile = open(log_file, 'wt+')

	Image_Path = evidence

	if(item_to_process == "Single File"):
		filename_to_process = evidence
		#set up foremost command
		if(not re.search('Configuration', options)):
			foremost_command = "foremost -d -o " + "'" + folder_path  + "/" + filename_to_process + "/unallocated_files" + "'" +" -t " + str(options) + " -i " + Image_Path

		else:
			foremost_command = "foremost -d -o " + "'" + folder_path + "/" + filename_to_process + "/unallocated_files" + "'" +" -c /etc/foremost.conf -i " + Image_Path
		print("The foremost_command is: " + foremost_command + "\n")

		#for a single file we don't need to run blkls, we just need to execute the foremost command
		#run foremost command
		subprocess.call([foremost_command], shell=True)
		
	elif(item_to_process == "Bit-Stream Image"):

		#check if Image file is in Encase format
		if re.search(".E01", Image_Path):
			#get datetime
			now = datetime.datetime.now()

			#set Mount Point
			mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S")
			#mount_point = "/mnt/"+case_number+"_unallocated"
			Image_Path = mount_ewf(Image_Path, outfile, mount_point)
		#call mmls function
		partition_info_dict, temp_time = mmls(outfile, Image_Path)
		#partition_info_dict_temp, temp_time = partition_info_dict

		#get filesize of mmls_output.txt
		file_size = os.path.getsize("/tmp/mmls_output_" + str(temp_time) + ".txt") 

		#if filesize of mmls output is 0 then run parted
		if(file_size == 0):
			print("mmls output was empty, running parted")
			outfile.write("mmls output was empty, running parted")
			#call parted function
			partition_info_dict, temp_time = parted(outfile, Image_Path)

		else:
	
			#read through the mmls output and look for GUID Partition Tables (used on MACS)
			mmls_output_file = open("/tmp/mmls_output_" + temp_time + ".txt", 'r')
			for line in mmls_output_file:
				if re.search("GUID Partition Table", line):
					print("We found a GUID partition table, need to use parted")
					outfile.write("We found a GUID partition table, need to use parted\n")
					#call parted function
					partition_info_dict, temp_time = parted(outfile, Image_Path)
			#close outfile
			mmls_output_file.close()

		#loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
		for key,value in partition_info_dict.items():
			#convert filesystem information into format required by foremost
			if(value == "hfs+"):
				value = "hfs"
			elif(value == "fat"):
				value = "fat16"

			#multiply key (offset) by 512 so it is in the right format for blkls
			key_bytes = int(key)//512

			#set up blkls command to gather unallocated clusters
			blkls_command = "blkls -A -f " + value + " -i raw -o " + str(key_bytes) + " " + Image_Path
			print("The blkls command is: " + blkls_command + "\n")
			outfile.write("The blkls command is: " + blkls_command + "\n")
	
			#set up foremost command
			if(not re.search('Configuration', options)):
				foremost_command = "foremost -d -o " + "'" + folder_path + "/Partition_" + str(key) + "/unallocated_files" + "'" +" -t " + str(options)
			else:
				foremost_command = "foremost -d -o " + "'" + folder_path  + "/Partition_" + str(key) + "/unallocated_files" + "'" +" -c /etc/foremost.conf"
			print("The foremost_command is: " + foremost_command + "\n")
			outfile.write("The foremost_command is: " + foremost_command + "\n")

			#set up command to pipe blkls through foremost
			pipe_command = blkls_command + "| " + foremost_command
			print("The pipe command is: " + pipe_command)
			outfile.write("The pipe command is: " + pipe_command)

			#run pipe command
			subprocess.call([pipe_command], shell=True)

			

	#run fdupes against output path to eliminate dupes
	remove_dupes_module_noask(evidence, outfile, folder_path)

	#close outfile
	outfile.close()
	

	#chdir to output foler
	os.chdir(folder_path)

	#run text files through unix2dos
	for root, dirs, files in os.walk(folder_path):
		for filenames in files:
			#get file extension
			fileName, fileExtension = os.path.splitext(filenames)
			if(fileExtension.lower() == ".txt"):
				full_path = os.path.join(root,filenames)
				quoted_full_path = "'" +full_path+"'"
				print("Running Unix2dos against file: " + filenames)
				unix2dos_command = "sudo unix2dos " + quoted_full_path
				subprocess.call([unix2dos_command], shell=True)

	#unmount and remove mount points
	if re.search(".E01", Image_Path):
		if(os.path.exists(mount_point+"_ewf")):
			subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
			os.rmdir(mount_point+"_ewf")


	#delete /tmp files
	if (os.path.exists("/tmp/mmls_output_" + temp_time + ".txt")):
		os.remove("/tmp/mmls_output_" + temp_time + ".txt")



