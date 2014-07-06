#!/usr/bin/env python3
#This program extracts file entries based on user entered
#file names in Over/Deleted/VSS Windows based Bit Stream Images

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2013 Chapin.Bryce@Mantech.com				 #
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
from remove_dupes_module_noask import *
from mmls import *
from Windows_Time_Converter_module import *
from check_for_folder import *


import os
from os.path import join
import re
import io
import sys
import string
import subprocess
import datetime
import shutil
import struct
import hashlib

### GET BLOCK SIZE ##############################################################################################
def get_block_size_mmls(Image_Path, outfile):
	block_size = subprocess.check_output(['mmls -i raw ' + Image_Path + " | grep Units | awk '{print $4}' | sed s/-byte//"], shell=True, universal_newlines=True)
	block_size = block_size.strip()
	print("The block size is: " + str(block_size))
	outfile.write("The block size is: " + str(block_size) + "\n\n")
	return block_size

def get_block_size_parted(outfile, temp_time):
	block_size_command = "sudo cat /tmp/timeline_partition_info_" + temp_time +".txt | grep -a " + "'"+"Sector size"+"'" + " | awk {'print $4'} | sed s_B/.*__"
	outfile.write("The block_size command is: " + block_size_command + "\n")
	block_size = subprocess.check_output([block_size_command], shell=True, universal_newlines=True)
	block_size = block_size.strip()
	print("The block size is: " + str(block_size))
	outfile.write("The block size is: " + str(block_size) + "\n\n")
	return block_size
### END GET BLOCK SIZE ##########################################################################################

### PROCESS FLS OUTPUT ###### ############################################################
def process_fls_output(value, key, Image_Path, block_size, folder_path, log_folder_path, out_folder, item, searchfile, outfile, temp_file):
	#divide offset by block size so it is in correct format for fls	
	key_bytes = int(key)//int(block_size)

	#open FLS output file
	fls_output_file = open(log_folder_path + "/" + temp_file + ".txt", 'r')
	
	for line in fls_output_file:

		#print current line for debugging purposes
		#print(line)

		newList=[]
		#strip carriage returns
		line = line.strip()
		
		line_split = line.split('/')
		#print(line_split)
		for i in line_split:
			newList.append(i.split('\t')[0])
		#print (newList)

		#assign items in newList to variables
		inode_number_temp = newList[1]

		#strip alpha chars from inode & leading space
		inode_number = re.sub('[a-z]','',inode_number_temp)
		inode_number = re.sub('^ +','', inode_number)			


		#get file_name
		file_name = newList[-1]

		if(item == "NO"):
			if(re.search('OrphanFiles', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + out_folder + "/" + inode_number + "_Partition_" + str(key) + "_" + searchfile +"_DELETED" + "'"
			else:
				#get user profile name
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + out_folder + "/" + inode_number + "_Partition_" + str(key) + "_OVERT_" + searchfile  + "'"
		else: #these are the shadow volume files
			if(re.search('OrphanFiles', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + out_folder + "/" + inode_number + "_Partition_" + str(key) + "_DELETED_" + searchfile + "_" + item + "'"
			else:
				#get user profile name
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + out_folder + "/" + inode_number + "_Partition_" + str(key) + "_" + searchfile + "_" + item + "'"

		print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10))
		outfile.write("The icat command is: " + icat_command + "\n")

		#run icat command
		subprocess.call([icat_command], shell=True)

	#close file	
	fls_output_file.close()	

##########################################################################################

### PROCESS OVERT / DELETED HIVES ##############################################################################

def process_overt_deleted_files(value, key, Image_Path, outfile, folder_path, log_folder_path, out_folder, block_size, item, temp_time, searchfile):
	#divide offset by block size so it is in correct format for fls	
	key_bytes = int(key)//int(block_size)

	searchfile = searchfile.strip("\n")
	
	if (item == "NO"):
		print("Partition")
		temp_file = "fls_output_ntfs_partition_" + str(key)

	else:
		print("VSS")
		temp_file = "fls_output_ntfs_" + item

	
	#run fls to get information for files
	fls_command = "fls -Fpr -f ntfs -i raw -o " + str(key_bytes) + " " + Image_Path + " | grep -i '" + searchfile + "' | sed s/:// | sed s/*// > "+ log_folder_path + "/"+ temp_file + ".txt"
	#print ("\nThe fls command is: " + fls_command + "\n")
	print("\nSearching...")
	outfile.write("The fls command is: " + fls_command + "\n")

	#run fls command
	subprocess.call([fls_command], shell=True)

	#process fls output
	process_fls_output(value, key, Image_Path, block_size, folder_path, log_folder_path, out_folder, item, searchfile, outfile, temp_file)
						
### END PROCESS OVERT / DELETED HIVES ##############################################################################



### CHECK FOR SHADOW VOLUMES ################################################

def check_for_shadow_volumes(Image_Path, key, block_size, outfile, folder_path, log_folder_path, out_folder, temp_time, searchfile):

	#set shadow volume variables
	has_shadow_volumes = "NULL"
	vssvolume_mnt = "NULL"

	#divide offset by block size so it is in correct format for vshadowinfo	
	key_bytes = int(key)//int(block_size)
	key_bytes_disk_offset = int(key) * int(block_size)
	image_no_quotes = Image_Path.replace("'","")
	print("\nChecking: " + Image_Path + " for shadow volumes")

	f = open('/tmp/dump_' + temp_time + '.txt', 'w+t')
	try:	
		vshadow_info_command = "vshadowinfo -v -o " + str(key) + " " + Image_Path
		#print("The vshadow_command is: " + vshadow_info_command)
		outfile.write("The vshadow_command is: " + vshadow_info_command)
		subprocess.call([vshadow_info_command], shell=True, stdout = f, stderr=subprocess.STDOUT)		
		#vshadow_output = subprocess.check_output([vshadow_info_command], shell=True, stderr=subprocess.STDOUT)
		f.close()

		f =open('/tmp/dump_' + temp_time + '.txt', 'rt')
		#print("try succedded")
		for line in f:
			line = line.strip()
			print(line)
			if (re.search("No Volume Shadow Snapshots found", line)):
				has_shadow_volumes = "NO"			

		if(has_shadow_volumes != "NO"):
			print("Partition at offset: " + str(key_bytes) + " has shadow volumes.")
			outfile.write("Partition at offset: " + str(key_bytes) + " has shadow volumes.")

			#check for existence of folder
			vssvolume_mnt = check_for_folder("/mnt/vssvolume", outfile)

			#mount shadow volumes for partition
			mount_shadow_command = "sudo vshadowmount -o " + str(key) + " " + Image_Path + " " + vssvolume_mnt
			print("The mount_shadow_command is: " + mount_shadow_command)

			subprocess.call(["sudo vshadowmount -o " + str(key) + " " + Image_Path + " " + vssvolume_mnt], shell=True, stderr=subprocess.STDOUT)

			#pass vssvolume mount point to mount_shadow_volume for mounting
			mount_shadow_volumes(vssvolume_mnt, outfile, folder_path, log_folder_path, out_folder, key, searchfile)

		elif(has_shadow_volumes == "NO"):
			print("Partition at offset: " + str(key) + " has no shadow volumes")
		
		f.close()

	except:
		print("The vshadow_info command for partition: " + str(key) + " failed")

	return vssvolume_mnt
#############################################################################

#### MOUNT INDIVIDUAL SHADOW VOLUMES ########################################

def mount_shadow_volumes(vssvolume_mnt, outfile, folder_path, log_folder_path, out_folder, key, searchfile):

	print("Inside mount_shadow_volumes sub")
	print("Vssvolume_mnt: " + vssvolume_mnt)

	#check for existence of folder
	vss_mount = check_for_folder("/mnt/vss_mount", outfile)

	vss_volumes = os.listdir(vssvolume_mnt)
	print(vss_volumes)

	for item in vss_volumes:
		print("About to process Shadow Volume: " + item)

		#Create Output Directory
		if not os.path.exists(folder_path + "/VSS_" + str(item)):
			os.makedirs(folder_path + "/VSS_" + str(item))
			
			outfile.write("Just created output folder: " + folder_path + "/VSS_" + str(item) + "\n\n")
		else:
			print("Output folder: " + folder_path +"/VSS_" + str(item) + " already exists")
			outfile.write("Output folder: " + folder_path +"/VSS_" + str(item) + " already exists\n\n")

		out_folder = folder_path +"/VSS_" + str(item)
		#call parted function
		partition_info_dict, temp_time = parted(outfile, vssvolume_mnt + "/"+item)
		block_size = get_block_size_parted(outfile, temp_time)
		for key,value in partition_info_dict.items():
			print("About to search for files in: " + item)
			process_overt_deleted_files(value, key, vssvolume_mnt+"/"+item, outfile, folder_path, log_folder_path, out_folder, block_size, item, temp_time, searchfile)
			

		
		
#############################################################################

### MAIN PROGRAM ########################################################################################################################
def filename_search_mr(item_to_process, case_number, root_folder_path, evidence, searchfile):
	print("The item to process is: " + item_to_process)
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)

	#get datetime
	now = datetime.datetime.now()

	#set Mount Point
	mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S")
	
	#create output folder path
	folder_path = root_folder_path + "/" + "Filename_Search"
	check_for_folder(folder_path, "NONE")
	
	#create Log Folder
	log_folder_path = folder_path + "/" + "Filename_Logs"
	check_for_folder(log_folder_path, "NONE")

	#open a log file for output
	log_file = log_folder_path + "/Filename_Search_Log.txt"
	outfile = open(log_file, 'wt+')

	Image_Path = '"' + evidence + '"'

	#set item variable to tell functions whether data is from shadow volumes
	item = "NO"

	#check if Image file is in Encase format
	if re.search(".E01", Image_Path):
		#set mount point
		mount_point = "/mnt/"+case_number+"_unallocated"
		Image_Path = mount_ewf(Image_Path, outfile, mount_point)


	#call mmls function
	partition_info_dict, temp_time = mmls(outfile, Image_Path)
	partition_info_dict_temp = partition_info_dict

	#get filesize of mmls_output.txt
	file_size = os.path.getsize("/tmp/mmls_output_" + temp_time + ".txt") 

	#if filesize of mmls output is 0 then run parted
	if(file_size == 0):
		print("mmls output was empty, running parted\n")
		outfile.write("mmls output was empty, running parted\n")
		#call parted function
		partition_info_dict, temp_time = parted(outfile, Image_Path)
		block_size = get_block_size_parted(outfile, temp_time)

	else:

		#get block_size since mmls was successful
		block_size = get_block_size_mmls(Image_Path, outfile)

		#read through the mmls output and look for GUID Partition Tables (used on MACS)
		mmls_output_file = open("/tmp/mmls_output_" + temp_time + ".txt", 'r')
		for line in mmls_output_file:
			if re.search("GUID Partition Table", line):
				print("We found a GUID partition table, need to use parted")
				outfile.write("We found a GUID partition table, need to use parted\n")
				#call parted function
				partition_info_dict, temp_time = parted(outfile, Image_Path)

	#loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
	for key,value in partition_info_dict.items():

		#process overt registy hives
		if(value =="ntfs") or (value=="fat32"):
			if not os.path.exists(folder_path + "/Partition_" + str(key)):
				os.makedirs(folder_path + "/Partition_" + str(key))
				#print("Just created output folder: " + folder_path + "/Partition_" + str(key))	
				outfile.write("Just created output folder: " + folder_path + "/Partition_" + str(key) + "\n\n")
			else:
				print("Output folder: " + folder_path +"/Partition_" + str(key) + " already exists")
				outfile.write("Output folder: " + folder_path +"/Partition_" + str(key) + " already exists\n\n")	
			
			#chande output dir
			out_folder = folder_path +"/Partition_" + str(key)

			process_overt_deleted_files(value, key, Image_Path, outfile, folder_path, log_folder_path, out_folder, block_size, item, temp_time, searchfile)
			vssvolume_mnt = check_for_shadow_volumes(Image_Path, key, block_size, outfile, folder_path, log_folder_path, out_folder, temp_time, searchfile)
		
		else:
			print("This partition is not formatted NTFS or FAT32")
			outfile.write("This partition is not formatted NTFS or FAT32\n\n")

	#run fdupes against output path to eliminate dupes
	remove_dupes_module_noask(folder_path, outfile, str(key))

	
	shutil.copyfile("/tmp/fdupes_duplicates_log.txt", log_folder_path + "/fdupes_duplicates_log.txt")

	#chdir to output foler
	os.chdir(folder_path)

	#unmount shadow volumes
	if(vssvolume_mnt != "NULL"):
		print("Unmounting: " + vssvolume_mnt)
		outfile.write("Unmounting: " + vssvolume_mnt + "\n")
		subprocess.call(['sudo umount -f ' + vssvolume_mnt], shell=True)
		os.rmdir(vssvolume_mnt)

	

	#unmount and remount points
	if re.search(".E01", Image_Path):
		if(os.path.exists(mount_point+"_ewf")):
			subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
			os.rmdir(mount_point+"_ewf")
	
	#remove empty directories
	for root, dirs, files in os.walk(folder_path, topdown = False):
		for directory in dirs:
			dir_path = os.path.join(root, directory)
			if not os.listdir(dir_path):
				outfile.write("Removing empty folder: " + dir_path + "\n")
				os.rmdir(dir_path)

	#close outfiles
	outfile.close()

	#add md5 later
#	for root, dirs, files in os.walk(folder_path):	
#		for f in files:
#			current_file = os.path.join(root,f)
#			H = hashlib.md5()
#			with open(current_file) as FIN:
#				H.update(FIN.read().encode('utf8'))
#				out_prep = current_file + H.hexdigest()
#				md5out.write(out_prep)
#	md5out.close()

	#delete temp files
	#os.remove('/tmp/fls_output_ntfs_' + temp_time + '.txt')
	
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




