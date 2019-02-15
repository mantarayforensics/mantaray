#!/usr/bin/env python3
#This program reads from a configuration file and then runs each av scanner in the conf file
#using the arguments in the conf file

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2011 dougkoster@hotmail.com					             #
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

### process_folder #######################################################################################

def process_folder(folder_to_process, output_folder_path, outfile, evidence_type, conf_file):
	#open conf file
	print("The conf_file path is: " + conf_file)
	infile = open(conf_file, 'r')

	#loop through conf_file
	for line in infile:
		print("The current line is: " + line)
		#skip lines that are commented out
		if not (re.search('^#',line)):
			#strip leading and trailing whitespace from input line
			line = line.strip()
			
			#split line on comma
			line_split = line.split(',')
			
			#grab av_scanner name
			av_scanner = line_split[0]
			print("The AV Scanner from the conf file is: " + av_scanner)
			
			#grab commaind line options
			command_line = line_split[1]

			#grab post_scanning cleanup command
			post_scan_arguments = line_split[2]
			post_scan_arguments = post_scan_arguments.strip()
			print("The post_scan_arguments are: " + post_scan_arguments)
			
			if(re.search("NONE", post_scan_arguments)):
				command_line_with_folder = command_line + " " + '"' + folder_to_process + '"' + " >> " + '"' + output_folder_path + "/" + av_scanner + "_Results_" + evidence_type + ".txt" + '"'
			if not(re.search("NONE", post_scan_arguments)):
				command_line_with_folder = command_line + " " + '"' + folder_to_process + '"' " " + post_scan_arguments + " >> " + '"' + output_folder_path + "/" + av_scanner + "_Results_" + evidence_type + ".txt" + '"'
			print("The command line is: " + command_line_with_folder)
			outfile.write("The command line is: " + command_line_with_folder + "\n")

			print("Scanning for viruses using scanner: " + av_scanner + "\n")
			subprocess.call([command_line_with_folder], shell=True)

	infile.close		

##########################################################################################################

def av_scanner_mr(item_to_process, case_number, root_folder_path, evidence, conf_file):
	
	print("The item to process is: " + item_to_process)
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)
	print("The configuration file is located at: " + conf_file)

	evidence_no_quotes = evidence
	evidence = '"' + evidence + '"'

	#get datetime
	now = datetime.datetime.now()

	#set Mount Point
	mount_point = "/mnt/" + "MantaRay_" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")
	
	#create output folder path
	output_folder_path = root_folder_path + "/" + "AV_Scanner"
	check_for_folder(output_folder_path, "NONE")
	

	#open a log file for output
	log_file = output_folder_path + "/AV_Scanner_logfile.txt"
	outfile = open(log_file, 'wt+')

	if(item_to_process == "Single File"):
		print("Please put your file in a folder and then scan the folder")

	elif(item_to_process == "Directory"):
		folder_to_process = evidence_no_quotes
		process_folder(folder_to_process, output_folder_path, outfile, "Directory", conf_file)
	elif(item_to_process =="EnCase Logical Evidence File"):
		file_to_process = evidence
		mount_point = mount_encase_v6_l01(case_number, file_to_process, outfile)
		process_folder(mount_point, output_folder_path, outfile, "LEF", conf_file)

		#umount
		if(os.path.exists(mount_point)):
			subprocess.call(['sudo umount -f ' + mount_point], shell=True)
			os.rmdir(mount_point)
	elif(item_to_process == "Bit-Stream Image"):
		Image_Path = evidence
		#process every file on every partition
		#get datetime
		now = datetime.datetime.now()

		#set Mount Point
		mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")

		#check if Image file is in Encase format
		if re.search(".E01", Image_Path):

			#strip out single quotes from the quoted path
			#no_quotes_path = Image_Path.replace("'","")
			#print("THe no quotes path is: " +  no_quotes_path)
			#call mount_ewf function
			Image_Path = mount_ewf(Image_Path, outfile,mount_point)


		#call mmls function
		partition_info_dict, temp_time = mmls(outfile, Image_Path)
		partition_info_dict_temp = partition_info_dict

		#get filesize of mmls_output.txt
		file_size = os.path.getsize("/tmp/mmls_output_" + temp_time + ".txt") 


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
			mmls_output_file.close()
			

		#loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
		for key,value in sorted(partition_info_dict.items()):

			#disable auto-mount in nautilis - this stops a nautilis window from popping up everytime the mount command is executed
			cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false"
			try:
				subprocess.call([cmd_false], shell=True)
			except:
				print("Autmount false failed")

			#call mount sub-routine
			success_code, loopback_device_mount = mount(value,str(key),Image_Path, outfile, mount_point)

			if(success_code):
				print("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
				outfile.write("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
			else:
		
				print("We just mounted filesystem: " + value + " at offset:" + str(key) + "\n")
				outfile.write("We just mounted filesystem: " + value + " at offset:" + str(key) + "\n")

				#call av_scanner function for each mount_point
				process_folder(mount_point, output_folder_path, outfile, "partition_offset_"+str(key), conf_file)
				print("We just finished scanning every file...sorting output")

				#unmount and remove mount points
				if(os.path.exists(mount_point)): 
					subprocess.call(['sudo umount -f ' + mount_point], shell=True)
					os.rmdir(mount_point)
				#unmount loopback device if this image was HFS+ - need to run losetup -d <loop_device> before unmounting
				if not (loopback_device_mount == "NONE"):
					losetup_d_command = "losetup -d " + loopback_device_mount
					subprocess.call([losetup_d_command], shell=True)

			

		#delete /tmp files created for each partition
		if (os.path.exists("/tmp/mmls_output_" + temp_time + ".txt")):
			os.remove("/tmp/mmls_output_" + temp_time + ".txt")

	#close logfile
	outfile.close()

	#remove mount points created for this program
	if(os.path.exists(mount_point)):
		os.rmdir(mount_point)
	if(os.path.exists(mount_point+"_ewf")):
		subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
		os.rmdir(mount_point+"_ewf")

#run text files through unix2dos
	for root, dirs, files in os.walk(output_folder_path):
		for filenames in files:
			#get file extension
			fileName, fileExtension = os.path.splitext(filenames)
			if(fileExtension.lower() == ".txt"):
				full_path = os.path.join(root,filenames)
				quoted_full_path = "'" +full_path+"'"
				print("Running Unix2dos against file: " + quoted_full_path)
				#unix2dos_command = "sudo unix2dos " + "'"+filenames+"'"
				unix2dos_command = "sudo unix2dos " + quoted_full_path
				subprocess.call([unix2dos_command], shell=True)

