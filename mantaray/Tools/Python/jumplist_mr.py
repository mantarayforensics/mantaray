#!/usr/bin/env python3
#Recurses an entire image file (or a folder)  and runs j[.pl (Harlan Carvey) against every JumpList file file
#OUTPUT: TLN fomratted file and timeline file

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2012 	dougkoster@hotmail.com			                 #
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
from done import *
from unix2dos import *
from check_for_folder import *

import os
import re
import io
import sys
import string
import subprocess
import shutil
import datetime

##### GET ACCOUNT PROFILE NAME ##########################################################################################################################
def get_account_profile_names(account, outfile):
	#Takes absolute path to Jumplist file and returns the profile name

	print("The account name passed to the function is: " + account)
	outfile.write("The account name passed to the function is: " + account + "\n")

	#get substring
	account_sub = account[:-105]
	outfile.write("The account-sub name passed to the function is: " + account_sub + "\n")


	#get length
	account_sub_string_length = len(account_sub)

	#find offset of rightmost slash
	rightmost_slash_location = account_sub.rindex('/')

	#calculate substring	
	username = account_sub[(rightmost_slash_location+1):account_sub_string_length]

	return username


##### GET ACCOUNT PROFILE NAME ##########################################################################################################################

def jumplist_mr(item_to_process, case_number, root_folder_path, evidence):


	print("The item to process is: " + item_to_process)
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)

	evidence = '"' + evidence + '"'

	#get datetime
	now = datetime.datetime.now()

	#set Mount Point
	mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S")
	
	#create output folder path
	folder_path = root_folder_path + "/" + "Jumplist_Parser"
	check_for_folder(folder_path, "NONE")
	

	#open a log file for output
	log_file = folder_path + "/Jumplist_Parser_logfile.txt"
	outfile = open(log_file, 'wt+')

	

	#select image to process
	Image_Path = evidence
	print("The image path is: " + Image_Path)

	#check to see if Image file is in Encase format
	if re.search(".E01", Image_Path):
		#strip out single quotes from the quoted path
		no_quotes_path = Image_Path.replace("'","")
		print("The no quotes path is: " + no_quotes_path)
		#call mount_ewf function
		Image_Path = mount_ewf(no_quotes_path, outfile, mount_point)

	#call mmls function
	partition_info_dict, temp_time = mmls(outfile, Image_Path)
	partition_info_dict_temp = partition_info_dict

	#get filesize of mmls_output.txt
	file_size = os.path.getsize("/tmp/mmls_output_" + temp_time +".txt") 
	print("The filesize is: " + str(file_size))

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

	#loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
	#for key,value in partition_info_dict.items():
	for key,value in sorted(partition_info_dict.items()):

		#disable auto-mount in nautilis - this stops a nautilis window from popping up everytime the mount command is executed
		cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false"
		try:
			subprocess.call([cmd_false], shell=True)
		except:
			print("Autmount false failed")

		#run mount command
		success_code, loopback_device_mount = mount(value,key,Image_Path, outfile, mount_point)

		if(success_code):
			print("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
			outfile.write("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
		else:
		
			print("We just mounted filesystem: " + value + " at offset:" + str(key) + ".\n")
			outfile.write("We just mounted filesystem: " + value + " at offset:" + str(key) + "\n")
		
			#run jl.pl against every JumpList file found under mount_point if filesystem is fat32 or ntfs
			if(value == "ntfs") or (value=="fat32"):
				for root, dirs, files in os.walk(mount_point):
					for filenames in files:
						#get file extension
						fileName, fileExtension = os.path.splitext(filenames)
						if(fileExtension.lower() == ".automaticdestinations-ms"):
							full_path = os.path.join(root,filenames)
							quoted_full_path = "'" +full_path+"'"
							print("Processing Jump List: " + filenames)
							outfile.write("Processing Jump List: " + filenames + "\n")

							#get profile name
							profile = get_account_profile_names(full_path, outfile)
							print("The profile is: " + profile)
							outfile.write("The profile is: " + profile + "\n")
			
							#process Jumplist files with jl.pl
							#jl_command = "perl /usr/share/windows-perl/jl.pl -u " + "'" + profile + "'" + " -f " + full_path + " >> " + "'" + folder_path + "/jumplist_metadata.txt" + "'"
							jl_command_tln = "perl /usr/share/windows-perl/jl.pl -u " + "'" + profile + "'" + " -t -f " + quoted_full_path + " >> " + "'" + folder_path + "/jumplist_metadata_tln.txt" + "'"
							outfile.write("The jl_command_tln is: " + jl_command_tln + "\n")
							subprocess.call([jl_command_tln], shell=True)
						else:
							print("Scanning file: " + filenames + ".  This file is not a jumplist.")
				#unmount and remove mount points
				if(os.path.exists(mount_point)): 
					subprocess.call(['sudo umount -f ' + mount_point], shell=True)
					os.rmdir(mount_point)
				#unmount loopback device if this image was HFS+ - need to run losetup -d <loop_device> before unmounting
				if not (loopback_device_mount == "NONE"):
					losetup_d_command = "losetup -d " + loopback_device_mount
					subprocess.call([losetup_d_command], shell=True)
			else:
				print("Filesystem: " + value + " at offset:" + str(key) + " is not NTFS or FAT32")
				outfile.write("Filesystem: " + value + " at offset:" + str(key) + " is not NTFS or FAT32\n")

				if(os.path.exists(mount_point)): 
					subprocess.call(['sudo umount -f ' + mount_point], shell=True)
					os.rmdir(mount_point)
				#unmount loopback device if this image was HFS+ - need to run losetup -d <loop_device> before unmounting
				if not (loopback_device_mount == "NONE"):
					losetup_d_command = "losetup -d " + loopback_device_mount
					subprocess.call([losetup_d_command], shell=True)
			#create timeline
			parse_command = "perl /usr/share/windows-perl/parse.pl -f " + "'" + folder_path + "/jumplist_metadata_tln.txt" + "'" + "> " + "'" + folder_path + "/jumplist_timeline.txt" + "'"
			subprocess.call([parse_command], shell=True)

	#unmount and remove mount points
	#if(os.path.exists(mount_point)):
	#	os.rmdir(mount_point)
	if(os.path.exists(mount_point+"_ewf")):
		print("Unmounting mount point for ewf before exiting\n\n")
		subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
		os.rmdir(mount_point+"_ewf")

	#program cleanup
	outfile.close()
	#convert outfile using unix2dos	
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
				print("Running Unix2dos against file: " + quoted_full_path)
				#unix2dos_command = "sudo unix2dos " + "'"+filenames+"'"
				unix2dos_command = "sudo unix2dos " + quoted_full_path
				subprocess.call([unix2dos_command], shell=True)



