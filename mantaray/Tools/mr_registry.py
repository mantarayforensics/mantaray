#!/usr/bin/env python3
#This program runs regripper (written by Harlan Carvey) for each registry hive found in a Disk Image
#Expects regripper to be located at: /usr/share/regripper/
#Expects regripper plugins to be located at: /usr/share/regripper/plugins/
#You will need to have text files located in /usr/share/regripper/plugins named sam, ntuser, system, security, software, usrclass
#These text files should contain the name of every plugin for that hive type that you want to run automatically
#For example... The file /usr/share/regripper/plugins/sam on my system contains one line that says "samparse".  This tells the program 
#that if it is processing a SAM hive it should run the regripper plugin samparse agains the SAM hive
#If you don't have these text files created the program will not produce any output.

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2011  dougkoster@hotmail.com				                 #
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
from Windows_Time_Converter_module import *

import os
from os.path import join
import re
import io
import sys
import string
import subprocess
import pickle
import datetime
import stat

### GET USER PROFILE NAME #######################################################################
def get_profile_name(file_name):
	file_name = '"' + file_name + '"'
	print("The filename is: " + file_name)
	#split on underscore
	file_name_list = file_name.split("_")
	profile = file_name_list[-2]	
	print("The user profile is: " + profile)

	return profile

### GET USER PROFILE NAME #######################################################################

### PROCESS USRCLASS HIVES ######################################################################

def process_usrclass(abs_file_path, usrclass_plugins, file_name, folder_path, outfile, evidence_type):
	if (evidence_type != "Directory"):
		profile_name = get_profile_name(abs_file_path)

	#get file metadata
	human_atime, MD5 = get_metadata(abs_file_path, file_name)

	#create folder for USRCLASS if it doesn't exist
	if not os.path.exists(folder_path + "/USRCLASS_INFO/"):
		os.mkdir(folder_path + "/USRCLASS_INFO/")
		print("Creating directory: " + folder_path + "/USRCLASS_INFO/")

	if (evidence_type != "Directory"):
		#create folder for USRCLASS profile if it doesn't exist
		if not os.path.exists(folder_path + "/USRCLASS_INFO/" + profile_name):
			os.mkdir(folder_path + "/USRCLASS_INFO/" + profile_name)
			print("Creating directory: " + folder_path + "/USRCLASS_INFO/" + profile_name)

	#process URSCLASS with plugins
	with open(usrclass_plugins) as fh:
		for line in fh:
			line = line.strip()

			if not (re.search("#", line)):

				#write out filename and atime to output file
				if (evidence_type != "Directory"):
					outfile_rr = open(folder_path + "/USRCLASS_INFO/" + profile_name + "/" + line + ".txt", 'a')
				else:
					outfile_rr = open(folder_path + "/USRCLASS_INFO/" + line + ".txt", 'a')
				outfile_rr.write("Last Modified Time: " + human_atime + "\n")
				outfile_rr.write("Filename: " + file_name + "\n")
				outfile_rr.write("MD5 SUM: " + MD5 + "\n")
			
				outfile_rr.close()

				#run regripperl plugin against file
				if(evidence_type != "Directory"):
					rip_command = "perl /usr/share/regripper/rip.pl -r "+ "'" + abs_file_path + "'" + " -p " + line +" >> " + "'" + folder_path + "/USRCLASS_INFO/" + profile_name + "/" + line + ".txt" + "'"
				else:
					rip_command = "perl /usr/share/regripper/rip.pl -r "+ "'" + abs_file_path + "'" + " -p " + line +" >> " + "'" + folder_path + "/USRCLASS_INFO/" + line + ".txt" + "'"
				outfile.write("The rip command is: " + rip_command + "\n")
			
				#run regripper command
				subprocess.call([rip_command], shell=True)

				if (evidence_type != "Directory"):
					outfile_rr = open(folder_path + "/USRCLASS_INFO/" + profile_name + "/" + line + ".txt", 'a')
				else:
					outfile_rr = open(folder_path + "/USRCLASS_INFO/" + line + ".txt", 'a')
				outfile_rr.write("\n-------------------------------------------------------------------------------------------\n\n")
				outfile_rr.close()

#################################################################################################

### PROCESS OTHER HIVES ######################################################################

def process_other_hives(abs_file_path, plugins, file_name, hive_name_info, folder_path, outfile):

	#get file metadata
	human_atime, MD5 = get_metadata(abs_file_path, file_name)

	#create folder for USRCLASS if it doesn't exist
	if not os.path.exists(folder_path + "/" + hive_name_info +"/"):
		os.mkdir(folder_path + "/" + hive_name_info +"/")
		print("Creating directory: " + folder_path + "/" + hive_name_info + "/")

	#process URSCLASS with plugins
	with open(plugins) as fh:
		for line in fh:
			
			line = line.strip()

			if not (re.search("#", line)):
				if line == "productpolicy" != "ProductName = Windows Vista (TM) Ultimate":
					pass
				else:
					#write out filename and atime to output file
					outfile_rr = open(folder_path + "/" + hive_name_info + "/" + line + ".txt", 'a')
					outfile_rr.write("Last Modified Time: " + human_atime + "\n")
					outfile_rr.write("Filename: " + file_name + "\n")
					outfile_rr.write("MD5 SUM: " + MD5 + "\n")
				
					outfile_rr.close()
	
					#run regripperl plugin against file
					rip_command = "perl /usr/share/regripper/rip.pl -r "+ "'" + abs_file_path + "'" + " -p " + line +" >> " + "'" + folder_path + "/" + hive_name_info + "/" + line + ".txt" + "'"
					outfile.write("The rip command is: " + rip_command + "\n")
				
					#run regripper command
					subprocess.call([rip_command], shell=True)
	
					outfile_rr = open(folder_path + "/" + hive_name_info + "/" + line + ".txt", 'a')
					outfile_rr.write("\n-------------------------------------------------------------------------------------------\n\n")
					outfile_rr.close()

#################################################################################################

### PROCESS NTUSER HIVES ######################################################################

def process_ntuser(abs_file_path, ntuser_plugins, file_name, folder_path, outfile, evidence_type):
	if (evidence_type != "Directory"):
		profile_name = get_profile_name(abs_file_path)

	#get file metadata
	human_atime, MD5 = get_metadata(abs_file_path, file_name)

	#create folder for USRCLASS if it doesn't exist
	if not os.path.exists(folder_path + "/NTUSER_INFO/"):
		os.mkdir(folder_path + "/NTUSER_INFO/")
		print("Creating directory: " + folder_path + "/NTUSER_INFO/")

	if (evidence_type != "Directory"):
		#create folder for USRCLASS profile if it doesn't exist
		if not os.path.exists(folder_path + "/NTUSER_INFO/" + profile_name):
			os.mkdir(folder_path + "/NTUSER_INFO/" + profile_name)
			print("Creating directory: " + folder_path + "/NTUSER_INFO/" + profile_name)

	

	#process URSCLASS with plugins
	with open(ntuser_plugins) as fh:
		for line in fh:
			line = line.strip()

			if not (re.search("#", line)):

				#write out filename and atime to output file
				if (evidence_type != "Directory"):
					outfile_rr = open(folder_path + "/NTUSER_INFO/" + profile_name + "/" + line + ".txt", 'a')
				else:	
					outfile_rr = open(folder_path + "/NTUSER_INFO/" + line + ".txt", 'a')
				outfile_rr.write("Last Modified Time: " + human_atime + "\n")
				outfile_rr.write("Filename: " + file_name + "\n")
				outfile_rr.write("MD5 SUM: " + MD5 + "\n")
				outfile_rr.close()
		
				if(evidence_type != "Directory"):	
					rip_command = "perl /usr/share/regripper/rip.pl -r "+ "'"+ abs_file_path + "'" + " -p " + line +" >> " + "'" + folder_path + "/NTUSER_INFO/" + profile_name + "/" + line + ".txt" + "'"
				else:
					rip_command = "perl /usr/share/regripper/rip.pl -r "+ "'"+ abs_file_path + "'" + " -p " + line +" >> " + "'" + folder_path + "/NTUSER_INFO/" + line + ".txt" + "'"
				outfile.write("The rip command is: " + rip_command + "\n")
			
				#run regripper command
				subprocess.call([rip_command], shell=True)

				if (evidence_type != "Directory"):
					outfile_rr = open(folder_path + "/NTUSER_INFO/" + profile_name + "/" + line + ".txt", 'a')
				else:
					outfile_rr = open(folder_path + "/NTUSER_INFO/" + line + ".txt", 'a')
				outfile_rr.write("\n-------------------------------------------------------------------------------------------\n\n")
				outfile_rr.close()


#################################################################################################

### GET METADATA ################################################################################

def get_metadata(abs_file_path, file_name):
	#get accessed time for filename

	print("\nProcessing File: " + abs_file_path)
	#atime = time.ctime(os.stat(abs_file_path).st_atime)

	#statinfo = os.stat(abs_file_path)
	#atime = statinfo.st_atime
	
	#get atime using ls command
	#ls_command = "ls -lt -ur " + abs_file_path + " | awk -F ' ' '{print $6, $7, $8}'"
	#atime = subprocess.check_output([ls_command], shell=True)

	#atime_decode = atime.decode(encoding='UTF-8')

	#big_edian_command
	big_endian_command = "hexdump -v -s 12 -n 8 -e " + "'" + "1/1 " + '"'+" %02X"+'"'+"'" + " " + "'" + abs_file_path + "'" + " | awk '{print $8$7$6$5$4$3$2$1}'"
	print("Temporal information for: " + file_name + ":")
	big_endian_time = subprocess.check_output([big_endian_command], shell=True)

	#call time converter python script
	windows_dt = Windows_Time_Converter_module(big_endian_time)
	atime = str(windows_dt).strip()
					
	print("Windows date/time is: " + str(atime) + "\n")

	#atime = os.path.getatime(abs_file_path)
	#print("The Last Modified Time for file: " + abs_file_path + " is: " + atime_decode)

	#convert to human readable form
	#dt = datetime.datetime.fromtimestamp(atime // 1000000000)
	#human_atime = dt.strftime('%Y-%m-%d %H:%M:%S')
	#print("The human atime is: " + str(human_atime))

	#get md5 hash for file
	md5 = subprocess.check_output(['md5sum ' + "'" + abs_file_path + "'" + " | awk '{print $1}'"], shell=True, universal_newlines=True)
	
	return str(atime), md5
#################################################################################################
def mr_registry(case_number, folder_to_process, root_folder_path, evidence_type):
	print("The case_name is: " + case_number)
	print("The evidence path is: " + folder_to_process)
	print("The output folder is: " + root_folder_path)
	print("The evidence type is: " + evidence_type)


	#if (evidence_type == "Directory"):
	#	#set folder_to_process
	#	folder_to_process = evidence_path

	#get datetime
	now = datetime.datetime.now()
	temp_time = now.strftime("%Y-%m-%d_%H_%M_%S_%f")
	
	#create output folder path
	folder_path = root_folder_path + "/" + "RegRipper"
	check_for_folder(folder_path, "NONE")
	
	#open a log file for output
	log_file = folder_path + "/RegRipper_logfile.txt"
	outfile = open(log_file, 'wt+')

	#set path to text files containing plugins to run for each hive type
	sam_plugins = "/usr/share/regripper/plugins/sam"
	ntuser_plugins = "/usr/share/regripper/plugins/ntuser"
	system_plugins = "/usr/share/regripper/plugins/system"
	software_plugins = "/usr/share/regripper/plugins/software"
	usrclass_plugins = "/usr/share/regripper/plugins/usrclass"
	security_plugins = "/usr/share/regripper/plugins/security"

	#read filename and atime into dictionary
	file_metadata = {}

	#run ls command against folder containing registry hives
	f = open('/tmp/ls_output_' + temp_time + '.txt', 'wt')
	os.chdir(folder_to_process)
	#ls_command = "ls -lt -ur " + "'" + folder_to_process + "'" + " | awk '{print $9, $10}'"
	ls_command = "ls -lt -ur . " + " | awk '{print $9, $10}'"
	print("The ls_command is: " + ls_command)
	try:
		subprocess.call([ls_command], shell=True, stdout = f, stderr=subprocess.STDOUT)
		f.close()
	except:
		print("Call to ls command failed")
		f.close()

	#initiating increment for counting
	counting_cmd = "ls -A " + folder_to_process + " | wc -l > /tmp/reg_count_files"	
	subprocess.call([counting_cmd], shell=True)
	counting_it = open('/tmp/reg_count_files', 'r')
	number_of_files = counting_it.readline()
	number_of_files = int(number_of_files)
	o = 0

	#read infile and process each file from oldest to youngest based on atime
	f = open('/tmp/ls_output_' + temp_time + '.txt', 'rt')
	for line in f:
		line = line.strip()
		file_name = line
		abs_file_path = os.path.join(folder_to_process,file_name)

		#process hives in ascending order based on atime
		if(re.search("USRCLASS", file_name.upper())):
			print("About to process file: " + file_name)
			process_usrclass(abs_file_path, usrclass_plugins, file_name, folder_path, outfile, evidence_type)
		elif(re.search("NTUSER", file_name.upper())):
			print("About to process file: " + file_name)
			process_ntuser(abs_file_path, ntuser_plugins, file_name, folder_path, outfile, evidence_type)
		elif(re.search("SAM", file_name.upper())):
			hive_name_info = "SAM_INFO"
			process_other_hives(abs_file_path, sam_plugins, file_name, hive_name_info, folder_path, outfile)
		elif(re.search("SOFTWARE", file_name.upper())):
			hive_name_info = "SOFTWARE_INFO"
			process_other_hives(abs_file_path, software_plugins, file_name, hive_name_info, folder_path, outfile)
		elif(re.search("SYSTEM", file_name.upper())):
			hive_name_info = "SYSTEM_INFO"
			process_other_hives(abs_file_path, system_plugins, file_name, hive_name_info, folder_path, outfile)
		elif(re.search("SECURITY", file_name.upper())):
			hive_name_info = "SECURITY_INFO"
			process_other_hives(abs_file_path, security_plugins, file_name, hive_name_info, folder_path, outfile)
		
		#Print Progress Percentage
		o = o + 1
		v = (o/number_of_files)*100
		print(v, "% complete")

	f.close()
	#close outfile
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
	if (os.path.exists("/tmp/ls_output_" + temp_time + ".txt")):
		os.remove("/tmp/ls_output_" + temp_time +".txt")
	
