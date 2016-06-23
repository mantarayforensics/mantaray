#!/usr/bin/env python3
#This program extracts all valid registry hives from a disk image (Overt, Deleted
#Unallocated, Shadow Volumes)

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2013 dougkoster@hotmail.com  							 #
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

### GET BLOCK SIZE ##############################################################################################
def get_block_size_mmls(Image_Path, outfile, temp_time):
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

### PROCESS FLS OUTPUT USRCLASS ############################################################
def process_fls_output_usrclass(value, key, Image_Path, block_size, folder_path, item, outfile, temp_time):
	#divide offset by block size so it is in correct format for fls	
	key_bytes = int(key)//int(block_size)

	#open FLS output file
	fls_output_file = open("/tmp/fls_output_" + temp_time + ".txt", 'r')
	
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
		inode_number = re.sub('[a-z]+','',inode_number_temp)
		inode_number = re.sub('\*', '', inode_number)
		inode_number = re.sub('^ +','', inode_number)
		inode_number = re.sub('\(', '', inode_number)
		inode_number = re.sub('\)','', inode_number)		
		
		user_name = newList[2]
		file_name = newList[-1]

		if(item == "NO"): #process non-shadow volume files

			if(re.search('OrphanFiles', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_ORPHAN_FILE" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10))
			elif(re.search('\*', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_DELETED_" + user_name + "_USRCLASS.DAT" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10) + "\t UserName: " + user_name.ljust(10))
			else:
				#get user profile name
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_OVERT_" + user_name + "_USRCLASS.DAT" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10) + "\t UserName: " + user_name.ljust(10))
		else: #these are the shadow volume files
			if(re.search('OrphanFiles', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_SHADOW_VOLUME_" + item + "_ORPHAN_FILE" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10))
			elif(re.search('\*', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_SHADOW_VOLUME_" + item + "_" + "DELETED_" + user_name + "_USRCLASS.DAT" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10) + "\t UserName: " + user_name.ljust(10))
			else:
				#get user profile name
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_SHADOW_VOLUME_" + item + "_" + "OVERT_" + user_name + "_USRCLASS.DAT" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10) + "\t UserName: " + user_name.ljust(10))

		

		outfile.write("The icat command is: " + icat_command + "\n")

		#run icat command
		subprocess.call([icat_command], shell=True)

	print("\n")

	#close file	
	fls_output_file.close()	

##########################################################################################

### PROCESS FLS OUTPUT NTUSER ############################################################
def process_fls_output_ntuser(value, key, Image_Path, block_size, folder_path, item, outfile, temp_time):
	#divide offset by block size so it is in correct format for fls	
	key_bytes = int(key)//int(block_size)

	#open FLS output file
	fls_output_file = open("/tmp/fls_output_" + temp_time + ".txt", 'r')
	
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
		inode_number = re.sub('[a-z]+','',inode_number_temp)
		inode_number = re.sub('\*', '', inode_number)
		inode_number = re.sub('^ +','', inode_number)
		inode_number = re.sub('\(', '', inode_number)
		inode_number = re.sub('\)','', inode_number)		
		
		user_name = newList[-2]
		file_name = newList[-1]

		if(item == "NO"):
			if(re.search('OrphanFiles', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_ORPHAN_FILE" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10))
			elif(re.search('\*', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_DELETED_" + user_name + "_NTUSER.DAT" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10) + "\t UserName: " + user_name.ljust(10))
			else:
				#get user profile name
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_OVERT_" + user_name + "_NTUSER.DAT" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10) + "\t UserName: " + user_name.ljust(10))
		else: #these are the shadow volumes
			if(re.search('OrphanFiles', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_SHADOW_VOLUME_" + item + "ORPHAN" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10))
			elif(re.search('\*', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_SHADOW_VOLUME_" + item + "_" + "_DELETED_" + user_name + "_NTUSER.DAT" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10) + "\t UserName: " + user_name.ljust(10))
			else:
				#get user profile name
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_SHADOW_VOLUME_" + item + "_" + "OVERT_" + user_name + "_NTUSER.DAT" + "'"
				print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10) + "\t UserName: " + user_name.ljust(10))

		
			
		outfile.write("The icat command is: " + icat_command + "\n")

		#run icat command
		subprocess.call([icat_command], shell=True)

	#close file	
	fls_output_file.close()	

##########################################################################################

### PROCESS FLS OUTPUT ###### ############################################################
def process_fls_output(value, key, Image_Path, block_size, folder_path, item, outfile, temp_time):
	#divide offset by block size so it is in correct format for fls	
	key_bytes = int(key)//int(block_size)

	#open FLS output file
	fls_output_file = open("/tmp/fls_output_" + temp_time + ".txt", 'r')
	
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
		inode_number = re.sub('[a-z]+','',inode_number_temp)
		inode_number = re.sub('\*', '', inode_number)
		inode_number = re.sub('^ +','', inode_number)
		inode_number = re.sub('\(', '', inode_number)
		inode_number = re.sub('\)','', inode_number)		


		#get file_name
		file_name = newList[-1]

		if(item == "NO"):
			if(re.search('OrphanFiles', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_ORPHAN_FILE" + "'"
			elif(re.search('\*', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_DELETED_" + file_name + "'"
			else:
				#get user profile name
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_OVERT_" + file_name + "'"
		else: #these are the shadow volume files
			if(re.search('OrphanFiles', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_SHADOW_VOLUME_" + item + "_ORPHAN_FILE_" + "'"
			elif(re.search('\*', line)):
				#copy files out using icat
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_SHADOW_VOLUME_" + item + "_DELETED_" + file_name + "'"			
			else:
				#get user profile name
				icat_command = "icat -r -i raw -f " + value + " -o " + str(key_bytes) + " -b " + block_size + " " + Image_Path + " " + inode_number + " > " + "'" + folder_path + "/" + inode_number + "_Partition_" + str(key) + "_SHADOW_VOLUME_" + item + "_OVERT_" + file_name + "'"

		print("File Name: " + file_name.ljust(10) + "\t" "Inode number: " + inode_number.ljust(10))
		outfile.write("The icat command is: " + icat_command + "\n")

		#run icat command
		subprocess.call([icat_command], shell=True)

	#close file	
	fls_output_file.close()	

##########################################################################################

### PROCESS OVERT / DELETED HIVES ##############################################################################

def process_overt_deleted_files(value, key, Image_Path, outfile, folder_path, block_size, item, file_loc, temp_time):

	#divide offset by block size so it is in correct format for fls	
	key_bytes = int(key)//int(block_size)



	#run fls to get information for OVERT NTUSER hives
	fls_command = "fls -Fpr -f ntfs -i raw -o " + str(key_bytes) + " " + Image_Path + " | grep -i 'ntuser.dat$\|_Registry_USER_NTUSER\|ntuser.bak$\|ntuser.sav$\|ntuser.old$' | grep -v -i log | sed s/:// > /tmp/fls_output_" + temp_time + ".txt"
	#print ("\nThe fls command is: " + fls_command + "\n")
	print("\nSearching for " + file_loc + " NTUSER hives")
	outfile.write("The fls command is: " + fls_command + "\n")

	#run fls command
	subprocess.call([fls_command], shell=True)

	#process fls output
	process_fls_output_ntuser(value, key, Image_Path, block_size, folder_path, item, outfile, temp_time)

	#run fls to get information for SYSTEM hives
	fls_command = "fls -Fpr -f ntfs -i raw -o " + str(key_bytes) + " " + Image_Path + " | grep -i 'system$\|system.sav$\|system.dat$\|system.old$\|system.bak$\|_Registry_Machine_SYSTEM$' | grep -v -i 'log\|FontCache-System.dat\|AnalyzeSystem' | sed s/:// > /tmp/fls_output_" + temp_time + ".txt"
	#print ("\nThe fls command is: " + fls_command + "\n")
	print("\nSearching for " + file_loc + " SYSTEM hives")
	outfile.write("The fls command is: " + fls_command + "\n")

	#run fls command
	subprocess.call([fls_command], shell=True)

	#process fls output
	process_fls_output(value, key, Image_Path, block_size, folder_path, item, outfile, temp_time)

	#run fls to get information for SOFTWARE hives
	fls_command = "fls -Fpr -f ntfs -i raw -o " + str(key_bytes) + " " + Image_Path + " | grep -i 'software$\|software.sav$\|software.dat$\|software.old$\|software.bak$\|_Registry_Machine_SOFTWARE$' | grep -v -i log | sed s/:// > /tmp/fls_output_" + temp_time + ".txt"
	#print ("\nThe fls command is: " + fls_command + "\n")
	print("\nSearching for " + file_loc + " SOFTWARE hives")
	outfile.write("The fls command is: " + fls_command + "\n")

	#run fls command
	subprocess.call([fls_command], shell=True)

	#process fls output
	process_fls_output(value, key, Image_Path, block_size, folder_path, item, outfile, temp_time)

	#run fls to get information for SECURITY hives
	fls_command = "fls -Fpr -f ntfs -i raw -o " + str(key_bytes) + " " + Image_Path + " | grep -i 'security$\|security.sav$\|security.dat$\|security.old$\|security.bak$\|_Registry_Machine_SECURITY$' | grep -v -i log | sed s/:// > /tmp/fls_output_" + temp_time + ".txt"
	#print ("\nThe fls command is: " + fls_command + "\n")
	print("\nSearching for " + file_loc + " SECURITY hives")
	outfile.write("The fls command is: " + fls_command + "\n")

	#run fls command
	subprocess.call([fls_command], shell=True)

	#process fls output
	process_fls_output(value, key, Image_Path, block_size, folder_path, item, outfile, temp_time)

	#run fls to get information for SAM hives (don't include files that end in .sam)
	fls_command = "fls -Fpr -f ntfs -i raw -o " + str(key_bytes) + " " + Image_Path + " | grep -i 'sam$\|sam.sav$\|sam.dat$\|sam.old$\|sam.bak$\|_Registry_Machine_SAM$' | grep -v -i 'log\|\.sam' | sed s/:// > /tmp/fls_output_" + temp_time + ".txt"
	#print ("\nThe fls command is: " + fls_command + "\n")
	print("\nSearching for " + file_loc + " SAM hives")
	outfile.write("The fls command is: " + fls_command + "\n")

	#run fls command
	subprocess.call([fls_command], shell=True)

	#process fls output
	process_fls_output(value, key, Image_Path, block_size, folder_path, item, outfile, temp_time)

	#run fls to get information for USRCLASS hives
	fls_command = "fls -Fpr -f ntfs -i raw -o " + str(key_bytes) + " " + Image_Path + " | grep -i 'usrclass.dat$\|_Registry_USER_USRCLASS\|usrclass.bak\|usrclass.sav\|usrclass.old' | grep -v -i log | sed s/:// > /tmp/fls_output_" + temp_time + ".txt"
	#print ("\nThe fls command is: " + fls_command + "\n")
	print("\nSearching for " + file_loc + " USRCLASS hives")
	outfile.write("The fls command is: " + fls_command + "\n")

	#run fls command
	subprocess.call([fls_command], shell=True)

	#process fls output
	process_fls_output_usrclass(value, key, Image_Path, block_size, folder_path, item, outfile, temp_time)

	
						
### END PROCESS OVERT / DELETED HIVES ##############################################################################

### PROCESS UNALLOCATED FILES ##############################################################################
def process_unallocated_clusters(value, key, Image_Path, outfile, case_number, folder_path, block_size):

	#convert filesystem information into format required by foremost
	if(value == "hfs+"):
		value = "hfs"
	elif(value == "fat"):
		value = "fat16"

	#multiply key (offset) by 512 so it is in the right format for blkls
	key_bytes = int(key)//int(block_size)

	#set up blkls command to gather unallocated clusters
	blkls_command = "blkls -A -f " + value + " -i raw -o " + str(key_bytes) + " " + Image_Path
	#print("\nThe blkls command is: " + blkls_command + "\n")
	outfile.write("\nThe blkls command is: " + blkls_command + "\n")
	
	foremost_command = "foremost -q -d -o " + "'" + folder_path  + "/Partition_" + str(key) + "/unallocated_files" + "'" +" -c /usr/share/Manta_Ray/Tools/conf_files/foremost.conf"
	#print("The foremost_command is: " + foremost_command + "\n")
	outfile.write("\nThe foremost_command is: " + foremost_command + "\n")

	#set up command to pipe blkls through foremost
	pipe_command = blkls_command + "| " + foremost_command
	#print("The pipe command is: " + pipe_command)
	outfile.write("\nThe pipe command is: " + pipe_command + "\n")

	#run pipe command
	print("\nProcessing unallocated clusters")
	subprocess.call([pipe_command], shell=True)

	for root, dirs, files in os.walk(folder_path):
		for filenames in files:
			fileName, fileExtension = os.path.splitext(filenames)
			abs_file_path = os.path.join(root,filenames)

			#get partition offset
			path_items = root.split("/")
			for item in path_items:
				if(re.search("Partition_", item)):
					partition_offset = item
					outfile.write("\nThe partition offset is: " + partition_offset + "\n")

			if(re.search("unallocated_files/dat/", abs_file_path)):
				destination = folder_path + "/" + partition_offset + "_Unallocated_" + filenames
				print("About to move and rename file: " + filenames)
				outfile.write("About to move and rename file: " + filenames + "\n")		
				os.rename(abs_file_path, destination)	

			elif(re.search("unallocated_files/audit.txt", abs_file_path)):
				destination = folder_path + "/" + partition_offset + "_" + filenames
				print("About to move and rename file: " + filenames)
				outfile.write("About to move and rename file: " + filenames + "\n")		
				os.rename(abs_file_path, destination)	
				
			
### END PROCEss UNALLOCATED FILES ##########################################################################

### CHECK FOR VALID REGISTRY HIVES ######################################
def check_for_valid_hives(folder_path, outfile):
	for root, dirs, files in os.walk(folder_path):
		for file_name in files:
			if not(re.search(".txt", file_name)):
				abs_file_path = os.path.join(root,file_name)
				#regfinfo_command = "regfinfo " + "'" + file_name + "'" + " | grep -m 1 Key"
				#print("The regfinfo_command is: " + regfinfo_command)
				try:
					regfinfo_return = subprocess.check_output(["regfinfo " +  "'" + abs_file_path + "'" + " | grep -q -m 1 Key"], shell=True, stderr=subprocess.STDOUT)
					print(file_name + ": is a valid registry hive")
				except subprocess.CalledProcessError:
					print("Deleting invalid registry file: " + file_name)
					outfile.write("\nDeleting invalid registry file: " + file_name + "\n")
					os.remove(abs_file_path)
					
	print("\n")

#########################################################################

### RESET REGISTRY HIVE TIMESTAMPS ##########################################################################

def reset_registry_hive_timestamps(folder_path, outfile):
	#reset timestamps
	for root,dirs,files in os.walk(folder_path):
		for file_name in files:
			
			abs_file_path = os.path.join(root,file_name)
			if re.search("Partition", file_name) and (os.path.getsize(abs_file_path) and not(re.search(".txt", file_name))):			
				#big_edian_command
				big_endian_command = "hexdump -v -s 12 -n 8 -e " + "'" + "1/1 " + '"'+" %02X"+'"'+"'" + " " + "'" + abs_file_path + "'" + " | awk '{print $8$7$6$5$4$3$2$1}'"
				outfile.write("\nThe big endian command is: " + big_endian_command + "\n") 
				print("Temporal information for: " + file_name + ":")
				big_endian_time = subprocess.check_output([big_endian_command], shell=True)

				#call time converter python script
				windows_dt = Windows_Time_Converter_module(big_endian_time)
				if(str(windows_dt).strip() != "1601-01-01 00:00:00"):
					
					print("Windows date/time is: " + str(windows_dt) + "\n")
					outfile.write("The Windows date/time for: " + file_name + " is: " + str(windows_dt) + "\n")

					#set up touch command
					touch_command = "touch -m -c -d " + str(windows_dt) + " " + "'" + abs_file_path + "'"
					#print("The touch command is: " + touch_command)
					
					subprocess.call([touch_command], shell=True, stderr=subprocess.STDOUT)
				else: # handle reg hives with no last accessed date
					if not os.path.exists(folder_path + "/Hives_Last_Accessed_Times_not_set"):
						os.makedirs(folder_path + "/Hives_Last_Accessed_Times_not_set")
						print("Just created output folder: " + folder_path + "/Hives_Last_Accessed_Times_not_set")
					
					#move file with no valid last access time
					destination = folder_path +"/Hives_Last_Accessed_Times_not_set/" + file_name
					print("About to move file with no last accessed time: " + file_name + " to: " + destination + "\n")
					outfile.write("About to move file with no last accessed time: " + abs_file_path + " to: " + destination)
					os.rename(abs_file_path, destination)	
					
					
#############################################################################################################

## GET HIVE TYPE ##########################################################

def get_hive_type(folder_path, outfile, temp_time, key):

	#make directory in /tmp so path name isn't so long
	temp_folder = "/tmp/hives_to_rename_"+temp_time
	print("The temp unallocated folder is: " + temp_folder)
	check_for_folder(temp_folder, outfile)	

	for file_name in os.listdir(folder_path):
		abs_file_path = os.path.join(folder_path, file_name)
		
		if re.search(str(key) + "_Unallocated", file_name) and (os.path.getsize(abs_file_path) and not(re.search(".txt", file_name))):
			#copy file to temp folder
			print("Copying file: " + abs_file_path + " to /tmp/hives_to_rename_" + temp_time)
			#outfile("Copying file: " + abs_file_path + " to /tmp/hives_to_rename_" + str(temp_time) +"\n")
			shutil.copy(abs_file_path, "/tmp/hives_to_rename_"+temp_time+"/"+file_name)
				
			#call get_hive_user_name
			get_hive_type_and_username(temp_time, file_name, outfile, abs_file_path, folder_path)

		elif re.search(str(key) + "_ORPHAN", file_name) and (os.path.getsize(abs_file_path) and not(re.search(".txt", file_name))):
			#copy file to temp folder
			print("Copying file: " + abs_file_path + " to /tmp/hives_to_rename_" + temp_time)
			#outfile("Copying file: " + abs_file_path + " to /tmp/hives_to_rename_" + str(temp_time) +"\n")
			shutil.copy(abs_file_path, "/tmp/hives_to_rename_"+temp_time+"/"+file_name)
				
			#call get_hive_user_name
			get_hive_type_and_username(temp_time, file_name, outfile, abs_file_path, folder_path)

	#delete temp folder
	if (os.path.exists("/tmp/hives_to_rename_" + temp_time)):
		shutil.rmtree("/tmp/hives_to_rename_" + temp_time)			
				

###########################################################################

### GET HIVE USERNAME #####################################################

def get_hive_type_and_username(temp_time, file_name, outfile, abs_file_path, folder_path):

	try:
		header_info = subprocess.check_output(["head -c 150 " + "'" + "/tmp/hives_to_rename_" + temp_time +"/" + file_name +  "'" + " | iconv -c -f UTF-16 -t UTF-8"], shell=True, stderr=subprocess.STDOUT)
		header_info_decoded = header_info.decode(encoding='UTF-8')

		print("The header info is: " + header_info_decoded)
		outfile.write("The header info is: " + header_info_decoded + "\n")

		if(re.search("usrclass", header_info_decoded.lower())):
			print("This hive is a USRCLASS.dat")
			outfile.write("This hive is a USRCLASS.dat\n")

			#run head command to get profile name
			head_command = "head -c 150 " + "'" + "/tmp/hives_to_rename_" + temp_time +"/" + file_name + "'" + " | iconv -c -f UTF-16 -t UTF-8 | egrep -iao " + "'" + "[/\][-[:alnum:][:space:]]*[/\]usrclass" + "'" + " | awk -F\\\\ '{print $2}'"

			usrclass_name = subprocess.check_output([head_command], shell=True, stderr=subprocess.STDOUT)

			#if the subprocess command resulted in a username
			if(usrclass_name):
				usrclass_name_decode = usrclass_name.decode(encoding='UTF-8')
				usrclass_name_decode = usrclass_name_decode.strip()

				print("The usrclass.dat username is: " + usrclass_name_decode)
			
				print(file_name + ": is USRCLASS.  USRCLASS name is: " + usrclass_name_decode + " -- renaming\n")
				outfile.write(file_name + ": is USRCLASS.  USRCLASS name is: " + usrclass_name_decode + " -- renaming\n")

				destination = abs_file_path + "_" + usrclass_name_decode + "_USRCLASS.dat"
				os.rename(abs_file_path, destination)
			else:
	
				print(file_name + ": is USRCLASS.  USRCLASS name is: UNKOWN -- renaming\n")
				outfile.write(file_name + ": is USRCLASS.  USRCLASS name is: UNKNOWN -- renaming\n")
				destination = abs_file_path + "_Unknown_UserName_USRCLASS.dat"
				os.rename(abs_file_path, destination)

		elif(re.search("ntuser", header_info_decoded.lower())):
			print("This hive is a NTUSER.dat")
			outfile.write("This hive is a NTUSER.dat\n")

			#run head command to get profile name
			head_command = "head -c 150 " + "'" + "/tmp/hives_to_rename_" + temp_time +"/" + file_name + "'" + " | iconv -c -f UTF-16 -t UTF-8 | egrep -iao " + "'" + "[/\][-[:alnum:][:space:]]*[/\]ntuser" + "'" + " | awk -F\\\\ '{print $2}'"

			ntuser_name = subprocess.check_output([head_command], shell=True, stderr=subprocess.STDOUT)

			#if the subprocess command resulted in a username
			if(ntuser_name):
				ntuser_name_decode = ntuser_name.decode(encoding='UTF-8')
				ntuser_name_decode = ntuser_name_decode.strip()

				print("The ntuser.dat username is: " + ntuser_name_decode)
			
				print(file_name + ": is NTUSER.  NTUSER name is: " + ntuser_name_decode + " -- renaming\n")
				outfile.write(file_name + ": is NTUSER.  NTUSER name is: " + ntuser_name_decode + " -- renaming\n")
	
				destination = abs_file_path + "_" + ntuser_name_decode + "_NTUSER.dat"
				os.rename(abs_file_path, destination)
			else:
	
				print(file_name + ": is NTUSER.  NTUSER name is: UNKOWN -- renaming\n")
				outfile.write(file_name + ": is NTUSER.  NTUSER name is: UNKNOWN -- renaming\n")
				destination = abs_file_path + "_Unknown_UserName_NTUSER.dat"
				os.rename(abs_file_path, destination)

		elif(re.search("system", header_info_decoded.lower())) and not (re.search("system32", header_info_decoded.lower())):
			print("This hive is a SYSTEM.dat")
			outfile.write("This hive is a SYSTEM.dat\n")

			destination = abs_file_path + ".SYSTEM"
			os.rename(abs_file_path, destination)

		elif(re.search("software", header_info_decoded.lower())):
			print("This hive is a SOFTWARE.dat")
			outfile.write("This hive is a SOFTWARE.dat\n")

			destination = abs_file_path + ".SOFTWARE"
			os.rename(abs_file_path, destination)

		elif(re.search("security", header_info_decoded.lower())):
			print("This hive is a SECURITY.dat")
			outfile.write("This hive is a SECURITY.dat\n")

			destination = abs_file_path + ".SECURITY"
			os.rename(abs_file_path, destination)

		elif(re.search("sam", header_info_decoded.lower())):
			print("This hive is a SAM.dat")
			outfile.write("This hive is a SAM hive\n")

			destination = abs_file_path + ".SAM"
			os.rename(abs_file_path, destination)

		else:
			print("This hive type is UNKNOWN")
			outfile.write("This hive type is UNKNOWN\n")

			destination = abs_file_path + ".UNKNOWN_Hive_Type"

			#create folder to hold unknown hive types
			if not os.path.exists(folder_path + "/Unknown_Hive_Type"):
				os.makedirs(folder_path + "/Unknown_Hive_Type")
				print("Just created output folder: " + folder_path + "/Unknown_Hive_Type")

			shutil.move(abs_file_path, folder_path + "/Unknown_Hive_Type/")

	except:

		print("The header information from this file could not be processed")
		outfile.write("The header information from this file could not be processed: " + file_name)
		destination = abs_file_path + ".UNKNOWN_Hive_Type"
		#create folder to hold unknown hive types
		if not os.path.exists(folder_path + "/Unknown_Hive_Type"):
			os.makedirs(folder_path + "/Unknown_Hive_Type")
			print("Just created output folder: " + folder_path + "/Unknown_Hive_Type")

		shutil.move(abs_file_path, folder_path + "/Unknown_Hive_Type/")

###########################################################################

### CHECK FOR SHADOW VOLUMES ################################################

def check_for_shadow_volumes(Image_Path, key, block_size, outfile, folder_path, temp_time):

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
		vshadow_info_command = "vshadowinfo -v -o " + str(key) + " " + Image_Path# + " > /tmp/dump.txt"
		#print("The vshadow_command is: " + vshadow_info_command)
		outfile.write("The vshadow_command is: " + vshadow_info_command)
		subprocess.call([vshadow_info_command], shell=True, stdout = f, stderr=subprocess.STDOUT)		
		#vshadow_output = subprocess.check_output([vshadow_info_command], shell=True, stderr=subprocess.STDOUT)
		#f.close()

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
			mount_shadow_volumes(vssvolume_mnt, outfile, folder_path, temp_time)

		elif(has_shadow_volumes == "NO"):
			print("Partition at offset: " + str(key) + " has no shadow volumes")
			
		f.close()

	except:
		print("The vshadow_info command for partition: " + str(key) + " failed")

	return vssvolume_mnt
#############################################################################

#### MOUNT INDIVIDUAL SHADOW VOLUMES ########################################

def mount_shadow_volumes(vssvolume_mnt, outfile, folder_path, temp_time):

	print("Vssvolume_mnt: " + vssvolume_mnt)

	#check for existence of folder
	vss_mount = check_for_folder("/mnt/vss_mount", outfile)

	vss_volumes = os.listdir(vssvolume_mnt)
	print(vss_volumes)
	for item in vss_volumes:
		print("Currently processing vss volume: " + item)
		#call parted function
		partition_info_dict, temp_time = parted(outfile, vssvolume_mnt + "/"+item)
		block_size = get_block_size_parted(outfile, temp_time)
		for key,value in partition_info_dict.items():
			print("About to process registry hives from: " + item)
			process_overt_deleted_files(value, key, vssvolume_mnt+"/"+item, outfile, folder_path, block_size, item, "SHADOW VOLUME", temp_time)
			
	#unmounting vss volume
	if(vssvolume_mnt != "NULL"):
		print("Unmounting: " + vssvolume_mnt)
		outfile.write("Unmounting: " + vssvolume_mnt + "\n")
		subprocess.call(['sudo umount -f ' + vssvolume_mnt], shell=True)
		os.rmdir(vssvolume_mnt)
		
#############################################################################

### MAIN PROGRAM ########################################################################################################################

def extract_registry_hives_mr(item_to_process, case_number, root_folder_path, evidence, options):
	print("The item to process is: " + item_to_process)
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)
	print("The options selected were: " + options)

	evidence = '"' + evidence + '"'

	#get datetime
	now = datetime.datetime.now()

	#set Mount Point
	mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")
	
	#create output folder path
	folder_path = root_folder_path + "/" + "Extracted_Registry_Hives"
	check_for_folder(folder_path, "NONE")
	

	#open a log file for output
	log_file = folder_path + "/Extracted_Registry_Hives_logfile.txt"
	outfile = open(log_file, 'wt+')

	Image_Path = evidence

	#set item variable to tell functions whether data is from shadow volumes
	item = "NO"

	#check if Image file is in Encase format
	if re.search(".E01", Image_Path):
		#set mount point
		#mount_point = "/mnt/"+	case_number+"_ewf"
		Image_Path = mount_ewf(Image_Path, outfile, mount_point)


	#call mmls function
	partition_info_dict, temp_time = mmls(outfile, Image_Path)
	partition_info_dict_temp = partition_info_dict

	#get filesize of mmls_output.txt
	file_size = os.path.getsize("/tmp/mmls_output_" + temp_time +".txt") 

	#if filesize of mmls output is 0 then run parted
	if(file_size == 0):
		print("mmls output was empty, running parted\n")
		outfile.write("mmls output was empty, running parted\n")
		#call parted function
		partition_info_dict, temp_time = parted(outfile, Image_Path)
		block_size = get_block_size_parted(outfile, temp_time)

	else:

		#get block_size since mmls was successful
		block_size = get_block_size_mmls(Image_Path, outfile, temp_time)

		#read through the mmls output and look for GUID Partition Tables (used on MACS)
		mmls_output_file = open("/tmp/mmls_output_" + temp_time + ".txt", 'r')
		for line in mmls_output_file:
			if re.search("GUID Partition Table", line):
				print("We found a GUID partition table, need to use parted")
				outfile.write("We found a GUID partition table, need to use parted\n")
				#call parted function
				partition_info_dict = parted(outfile, Image_Path)
		mmls_output_file.close()

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
			if(re.search("Unallocated", options)):
				process_unallocated_clusters(value, key, Image_Path, outfile, case_number, folder_path, block_size)
			if(re.search("Overt", options)):		
				process_overt_deleted_files(value, key, Image_Path, outfile, folder_path, block_size, item, "OVERT/DELETED", temp_time)
			if(re.search("Shadow", options)):			
				vssvolume_mnt = check_for_shadow_volumes(Image_Path, key, block_size, outfile, folder_path, temp_time)
			
			check_for_valid_hives(folder_path, outfile)
			get_hive_type(folder_path, outfile, temp_time, key)
			reset_registry_hive_timestamps(folder_path, outfile)
		
		else:
			print("This partition is not formatted NTFS or FAT32")
			outfile.write("This partition is not formatted NTFS or FAT32\n\n")

	#run fdupes against output path to eliminate dupes
	remove_dupes_module_noask(folder_path, outfile, str(key))

	#chdir to output foler
	os.chdir(folder_path)	

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

	#delete /tmp/ls_output.txt
	if (os.path.exists("/tmp/mmls_output_" + temp_time + ".txt")):
		os.remove("/tmp/mmls_output_" + temp_time + ".txt")
	if (os.path.exists("/tmp/timeline_partition_info_" + temp_time +".txt")):
		os.remove("/tmp/timeline_partition_info_" + temp_time +".txt")
	if (os.path.exists("/tmp/dump_" + temp_time + ".txt")):
		os.remove("/tmp/dump_" + temp_time + ".txt")
	if (os.path.exists("/tmp/fls_output_" + temp_time + ".txt")):
		os.remove("/tmp/fls_output_" + temp_time + ".txt")
	if (os.path.exists("/tmp/hives_to_rename_" + temp_time)):
		shutil.rmtree("/tmp/hives_to_rename_" + temp_time)
	
	

	return(folder_path)
