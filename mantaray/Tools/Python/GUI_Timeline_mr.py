#!/usr/bin/env python3
#This program automates the process of creating a super-timeline against a DD image or .E01 image
#It reads the partition table and runs Log2timeline (Kristinn Gudjonsson.) , FLS (Brian Carrier) and MACTIME (Brian Carrier) against each partition
#The timezone is determined for each partition.  If no timezone is present the program attempts to determine which timezone should be used.
#The script works against NTFS, FAT32, FAT16, FAT12, EXT2/3/4, HFS+ (Windows, Linux, MAC)

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2011 dougkoster@hotmail.com				                 #
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
from timezone_setting import *
from get_case_number import *
from get_output_location import *
from select_file_to_process import *
from select_folder_to_process import *
from parted import *
from mount import *
from mount_ewf import *
from get_ntuser_paths import *
from get_system_paths import *
from done import *
from unix2dos import *
from mmls import *
from parse_timeline_module import *
from mount_encase_v6_l01 import *
from check_for_folder import *
import os
from os.path import join
import re
import io
import sys
import string
import subprocess
import datetime

### SPLIT CSV ####################################################

def split_csv(case_number, temp_time_wc, folder_path, outfile, timeline_type):
	
	if(timeline_type == "l2t"):
		word_count_command = "wc -l " + case_number + "_timeline_modules.csv | awk '{print $1}' > /tmp/wc_" + temp_time_wc + ".txt"	
	elif(timeline_type == "plaso"):
		word_count_command = "wc -l " + case_number + "_timeline.csv | awk '{print $1}' > /tmp/wc_" + temp_time_wc + ".txt"
	lines = (subprocess.call([word_count_command], shell=True))

	fh = open('/tmp/wc_' + temp_time_wc + '.txt')

	for line in fh:
		#strip trailing carriage return
		line = line.strip()
		
		#since there is only one line in the input file we can now figure out if the file needs to be split
		#if the line has between 1M and 2M lines then divide the number of lines by 2 to determine where to split
		if(int(line) > 1000000) and (int(line) < 2000000):
			print("There are " + str(line) + " in this output file, so it needs to be split")
			outfile.write("There are " + str(line) + " in this output file, so it needs to be split\n\n")
			#figure out what number to use in the split command
			split_number = (int(line)//2) + 1

			#set up the split command
			if(timeline_type == "l2t"):
				split_command = "split -l " + str(split_number) + " " + case_number + "_timeline_modules.csv"
			elif(timeline_type == "plaso"):
				split_command = "split -l " + str(split_number) + " " + case_number + "_timeline.csv"
			print ("The split command is: " + split_command)
			outfile.write("The split command is: " + split_command + "\n\n")
			subprocess.call([split_command], shell=True)

			#rename files output from split command
			for root,dirs,files in os.walk(folder_path):
				for filenames in files:
					if re.search("xaa", filenames):
						#the first split file already contains the correct header line so just rename it
						if(timeline_type == "l2t"):
							os.rename(filenames, case_number + "_timeline_modules_split_"+filenames+".csv")
						elif(timeline_type == "plaso"):
							os.rename(filenames, case_number + "_timeline_split_"+filenames+".csv")
					elif re.search("xa", filenames):
						full_path = os.path.join(root, filenames)
						#add header info back into split file
						if(timeline_type == "l2t"):
							sed_command = "sed -i '1i\ Date,Size,Type,Mode,UID,GID,Meta,L2T_Function,File_Name' " + "'"+full_path+"'"
							
						elif(timeline_type == "plaso"):
							sed_command = "sed -i '1i\ Date,Time,Timezone,MACB,Source,SourceType,Type,User,Host,Short,Desc,Version,Filename,Inode,Notes,Format,Extra' " + "'" + full_path + "'"		
						subprocess.call([sed_command], shell=True)
						if(timeline_type == "l2t"):
							os.rename(filenames, case_number + "_timeline_modules_split_"+filenames+".csv")
						elif(timeline_type == "plaso"):
							os.rename(filenames, case_number + "_timeline_split_"+filenames+".csv")				
					

		elif(int(line) > 2000000):
			#if timeline is greater than 2M lines we need to divdide by 1000001
			#figure out what number to use in the split command
			split_number = (int(line)//1000001)
			split_number_final = (int(line)//(int(split_number)+int(1)))
			print("There are " + str(line) + " lines in this output file, so it needs to be split")
			outfile.write("There are " + str(line) + " lines in this output file, so it needs to be split")
			print("We are going to split the file at line: " + str(split_number_final))
			outfile.write("We are going to split the file at line: " + str(split_number_final) + "\n\n")

			#set up the split command
			if(timeline_type == "l2t"):
				split_command = "split -l " + str(split_number_final) + " " + case_number + "_timeline_modules.csv"
			elif(timeline_type == "plaso"):
				split_command = "split -l " + str(split_number_final) + " " + case_number + "_timeline.csv"
			print ("The split command is: " + split_command)
			outfile.write("The split command is: " + split_command + "\n\n")
			subprocess.call([split_command], shell=True)
			
			#rename files output from split command
			for root,dirs,files in os.walk(folder_path):
				for filenames in files:
					if re.search("xaa", filenames):
						#the first split file already contains the correct header line so just rename it
						if(timeline_type == "l2t"):
							os.rename(filenames, case_number + "_timeline_modules_split_"+filenames+".csv")
						if(timeline_type == "plaso"):
							os.rename(filenames, case_number + "_timeline_split_"+filenames+".csv")
					elif re.search("xa", filenames):
						full_path = os.path.join(root, filenames)
						#add header info back into split file
						if(timeline_type == "l2t"):
							sed_command = "sed -i '1i\ 	Date,Size,Type,Mode,UID,GID,Meta,L2T_Function, File_Name' " + "'"+full_path+"'"
						elif(timeline_type == "plaso"):
							sed_command = "sed -i '1i\ 	Date,Size,Type,Mode,UID,GID,Meta,L2T_Function, File_Name' " + "'"+full_path+"'"
						subprocess.call([sed_command], shell=True)
						if(timeline_type == "l2t"):
							os.rename(filenames, case_number + "_timeline_modules_split_"+filenames+".csv")
						elif(timeline_type == "plaso"):
							os.rename(filenames, case_number + "_timeline_split_"+filenames+".csv")

		else:
			outfile.write("There are: " + str(lines) + " in the supertimeline" + "\n")


### SPLIT CSV ######################################################

### GET ACCOUNT PROFILE NAMES #####################################

def get_account_profile_names(account):

	#This function takes the absolute path of the NTUSER.DAT file within a user's profile and returns the profile name
	#Example: If you pass the function this string: -> /mnt/windows_mount/Documents and Settings/Mr. Evil/NTUSER.DAT
	#it returns -> Mr. Evil

	#get substring to strip out /NTUSER.DAT from the string
	account_sub = account[:-11]

	#get length of account_sub
	account_sub_string_length = len(account_sub)

	#now that we have the length of the root string we need to find the offset of the last "/" in the string, then do a substring from that location
	#to the end of the string to get the user profile name
	rightmost_slash_location = account_sub.rindex('/')

	#calculate substring to just pull out the user name
	username = account_sub[(rightmost_slash_location+1):account_sub_string_length]
	username_quoted = "'" +username +"'"
	return username_quoted	
	
	
### GET ACCOUNT PROFILE NAMES #####################################

#### GET TIMEZONES NON WINDOWS ###########################

def get_timezones_non_windows(value, system_hive_path, outfile, mount_point):

	#get datetime
	now = datetime.datetime.now()
	temp_time_mac = now.strftime("%Y-%m-%d_%H_%M_%S_%f")
	
	#initialize timezone_final
	timezone_final = "NONE"

	if(value == "hfs+"):
		#for MAC systems get the timezone
		timezone_command = "ls -al " + "'" + mount_point + "/etc/localtime" + "'" + " |cut " + "'" + '-d/' + "'" + " -f9,10 > /tmp/timezone_mac_" + temp_time_mac
		print("The timezone_command is: " + timezone_command)
		subprocess.call([timezone_command], shell=True)

		#process output from tmp folder
		file_size = os.path.getsize("/tmp/timezone_mac_" + temp_time_mac)
		if(file_size != 0):
			fh = open("/tmp/timezone_mac_"+temp_time_mac)
			for line in fh:
				line = line.strip()
				timezone_final = line

			#fh close
			fh.close()

		print("The timezone final is: " + timezone_final)

	else: 
		#get the last line of /etc/localtime which should have the timezone
		last_line = "tail --lines=1 " + mount_point + "/etc/localtime > /tmp/timezone_linux_"+temp_time_mac

		#run the last_line command
		timezone_temp = subprocess.call([last_line], shell=True)
		if(timezone_temp != 1):
			fh = open('/tmp/timezone_linux_'+temp_time_mac)

			for line in fh:
				#split the line on comma
				timezone_split = line.split(',')

				#grab the first entry in timezone_split as the final timezone
				timezone_final = timezone_split[0]

			#fh close
			fh.close()
		else:
			timezone_final = "NONE"
	
	print ("The timezone for this non-windows drive is: "+ str(timezone_final), end = "\n\n")
	if(outfile != "NONE"):
		outfile.write("The timezone for this non-windows drive is: "+ str(timezone_final) + "\n\n")

	#return timezones
	return timezone_final
#### GET TIMEZONES NON WINDOWS ###########################

#### GET TIMEZONES WINDOWS ##############################
def get_timezones_windows(value, system_hive_path, outfile):
	#set timezone counter
	counter_timezone = 0;

	#get datetime
	now = datetime.datetime.now()
	temp_time_windows = now.strftime("%Y-%m-%d_%H_%M_%S_%f")

	#initialize variables
	timezone_final = "NONE"

	#set up regp command
	regp_command = "perl /usr/share/windows-perl/regp.pl "+ system_hive_path +" | grep -a 'StandardName;REG_SZ' > /tmp/regp_output_" + temp_time_windows + ".txt"
	print("The regp command is: " + regp_command + "\n\n")
	if(outfile != "NONE"):
		outfile.write("The regp command is: " + regp_command + "\n\n")

	#run the regp command
	print("about to call the subprocess to run regp_command\n")
	subprocess.call([regp_command], shell=True)
	print("just finished calling regp_command\n")

	fh_regp = open('/tmp/regp_output_' + temp_time_windows +'.txt', 'rt+', errors = 'ignore')

	for line in fh_regp:

		#strip trailing carriage return
		line = line.strip()

		#print ("The current entry in the Timezone list is: " + line)
		if(re.search('tzres.dll',line.lower())):
			print("This partition is not Windows XP, looking for timezone")
			if(outfile != "NONE"):
				outfile.write("This partition is not Windows XP, looking for timezone\n")
			regp_command_vista = "perl /usr/share/windows-perl/regp.pl " + system_hive_path +" | grep -a 'TimeZoneKeyName' > /tmp/regp_output_nonXP_" + temp_time_windows + ".txt"
				
			#run the regp command
			subprocess.call([regp_command_vista], shell=True)
		
			#open text file containing timezone information for non-XP partition			 	
			fh1 = open('/tmp/regp_output_nonXP_' + temp_time_windows + '.txt','rt+', errors = 'ignore')
			for line in fh1:
				line = line.strip()
				if(counter_timezone == 0):
					if(re.search('TimeZoneKeyName;REG_SZ',line)):
						timezone_final=timezone_setting(line)
						counter_timezone+=1
						print("The timezone_final for this nonXP partition is: " + str(timezone_final))
						if(outfile != "NONE"):
							outfile.write("The timezone_final for this nonXP partition is: " + str(timezone_final) + "\n")
		else:
			
			for line in fh_regp:
				if(counter_timezone == 0):
					timezone_final = timezone_setting(line)
					print("The timezone for this XP partition is: " + str(timezone_final) + "\n\n")
					if(outfile != "NONE"):
						outfile.write("The timezone for this XP partition is: " + str(timezone_final) + "\n")
					counter_timezone += 1

	fh_regp.close()
	return timezone_final
#### GET TIMEZONES WINDOWS ##############################


### LOG2TIMELINE ######################################################################

def log2timeline(timezone_shift, key, folder_path, outfile, mount_point):

	if(timezone_shift == "NONE"):
		#set log2timeline command
		log2timeline_command = "perl /usr/share/log2timeline/log2timeline_legacy -v -z UTC -o mactime -m Partition_" + key + " -r " +mount_point + " -log " + "'" + folder_path +"/bodyfile_" + key + "_log2timeline_log.txt" + "'" +" -d -w " + "'" + folder_path +"/bodyfile_" + key + "'"
		print ("The log2timeline command is: " + log2timeline_command, end ="\n\n")
		print ("Running Log2timeline against: " + mount_point, end ="\n\n")
		if(outfile != "NONE"):
			outfile.write("The log2timeline command is: " + log2timeline_command + "\n\n")
	else:
		#set log2timeline command
		log2timeline_command = "perl /usr/share/log2timeline/log2timeline_legacy -v -z " + timezone_shift + " -o mactime -m Partition_" + key + " -r " +mount_point + " -log " + "'" + folder_path +"/bodyfile_" + key + "_log2timeline_log.txt" + "'" +" -d -w " + "'" + folder_path +"/bodyfile_" + key + "'"
		print ("The log2timeline command is: " + log2timeline_command, end ="\n\n")
		print ("Running Log2timeline against: " + mount_point, end ="\n\n")
		if(outfile != "NONE"):
			outfile.write("The log2timeline command is: " + log2timeline_command + "\n\n")

	#run the log2timeline command
	subprocess.call([log2timeline_command], shell=True)

### LOG2TIMELINE ######################################################################

### PLASO ############################################################################

def plaso(key, folder_path, outfile, Image_Path, timezone_shift, plaso_output_options, case_number, cores_to_use):
#add logfile
	#convert cores_to_use to str
	cores_to_use = str(cores_to_use)

	#set plaso command
	if(timezone_shift == "NONE"):
		plaso_command = "log2timeline.py -o " + key + " -z UTC -t '" + case_number + "_Partition_" + key + "_' --vss --workers " + cores_to_use + " --logfile '" + folder_path + "/Timeline_Logs/plaso_logfile" + key + ".txt' '" + folder_path +"/partition_" + key + ".dmp" + "'" +" " + Image_Path + "" 
	else:
		plaso_command = "log2timeline.py -o " + key + " -z " + timezone_shift + " -t '" + case_number + "_Partition_" + key + "_' --vss --workers " + cores_to_use + " --logfile '" + folder_path + "/Timeline_Logs/plaso_logfile" + key + ".txt' '" + folder_path +"/partition_" + key + ".dmp" + "'" +" " + Image_Path + ""
	print ("The Plaso command is: " + plaso_command + "\n\n")
	print ("Running Plaso against: " + Image_Path + "\n\n")
	if(outfile != "NONE"):
		outfile.write("The plaso command is: " + plaso_command + "\n\n")

	#run the plaso command
	subprocess.call([plaso_command], shell=True)

	#setup psort options
	
	
	plaso_output_options = plaso_output_options.strip()
	plaso_output_options_split = plaso_output_options.split(",")

	plaso_output_options_split_len = len(plaso_output_options_split)
	print("plaso_output_options = ", plaso_output_options_split_len)

	run_l2tcsv = "False"
	run_sqlite = "False"
	run_elastic = "False"

	check_plaso_output = 0
	while check_plaso_output != plaso_output_options_split_len: 
		if plaso_output_options_split[check_plaso_output] == "CSV":
			print("l2tcsv ", plaso_output_options_split)
			run_l2tcsv = "True"
			check_plaso_output += 1
		elif plaso_output_options_split[check_plaso_output] == "SQLite":
			print("SQLite ", plaso_output_options_split)
			run_sqlite = "True"
			check_plaso_output += 1
		elif plaso_output_options_split[check_plaso_output] == "Elastic":
			print("Elastic ", plaso_output_options_split)
			run_elastic = "True"
			check_plaso_output += 1
		else:
			print("all ", plaso_output_options_split)
			run_l2tcsv = "False"
			run_sqlite = "False"
			run_elastic = "False"
			check_plaso_output += 1

	if run_l2tcsv == "False" and run_sqlite == "False" and run_elastic == "False":
		print("No output type selected for plaso. Saving dump file")



	#set & run pinfo command
	pinfo_cmd = "pinfo.py -v '" + folder_path + "/partition_" + key + ".dmp' > '" + folder_path + "/pinfo_partition_" + key + ".txt'"
	print ("The Plaso Pinfo command is: " + pinfo_cmd + "\n\n")
	if(outfile != "NONE"):
		outfile.write("The Plaso Pinfo command is: " + pinfo_cmd +"\n\n")
	subprocess.call([pinfo_cmd], shell=True)

	#set & run psort csv command
	if run_l2tcsv == "True":
		psort_cmd = "psort.py -o L2tcsv -z " + timezone_shift + " -w '" + folder_path + "/partition_" + key + "_timeline.csv' '" + folder_path + "/partition_" + key + ".dmp" + "'"
		print ("The Plaso Psort command is: " + psort_cmd + "\n\n")
		if(outfile != "NONE"):
			outfile.write("The Plaso Psort command is: " + psort_cmd + "\n\n")
		subprocess.call([psort_cmd], shell=True)

	#set & run psort sqlite command
	if run_sqlite == "True":
		psort_cmd = "psort.py -o Sql4n6 -z " + timezone_shift + " -w '" + folder_path + "/partition_" + key + "_sqlite' '" + folder_path + "/partition_" + key + ".dmp" + "'"
		print ("The Plaso Psort command is: " + psort_cmd + "\n\n")
		if(outfile != "NONE"):
			outfile.write("The Plaso Psort command is: " + psort_cmd + "\n\n")
		subprocess.call([psort_cmd], shell=True)

	#set & run psort Elastic command
	if run_elastic == "True":
		psort_cmd = "psort.py -o dynamic -z " + timezone_shift + " -w '" + folder_path + "/partition_" + key + "_timeline_dynamic.csv' '" + folder_path + "/partition_" + key + ".dmp'"
		print ("The Plaso Psort command is: " + psort_cmd + "\n\n")
		if(outfile != "NONE"):
			outfile.write("The Plaso Psort command is: " + psort_cmd + "\n\n")
		subprocess.call([psort_cmd], shell=True)
### PLASO ############################################################################


### FLS ##############################################################################

def fls(key, folder_path, value, outfile, Image_Path, timezone_final):

	#initialize variables
	fls_value = ""
	
	#modify filesystem values so they work with fls command
	if(value == "hfs+"):
		fls_value = "hfs"
	elif(value == "	msdos"):
		fls_value = "fat16"
	elif(value == "Apple"):
		fls_value = "hfs"
	else: fls_value = value

	#calculate partition start in sectors for fls command
	sector = int(key)//int(512)		

	#set up the fls command
	fls_command = "fls -z " + timezone_final + " -o " + str(sector) + " -f " + fls_value + " -r -i raw -m Partition_Offset_" + key + " " + Image_Path + ">> " + "'" + folder_path + "/bodyfile_" + key + "'"

	print("The fls command is: " + fls_command, end ="\n\n")
	if(outfile != "NONE"):
		outfile.write("The fls command is: " + fls_command + "\n\n")

	#run the fls command
	subprocess.call([fls_command], shell=True)
	
### FLS ##############################################################################

### REGTIME ##############################################################################
def regtime(system_hive_path, system_hive_regback_path, sam_hive_path, sam_hive_regback_path, security_hive_path, security_hive_regback_path, software_hive_path, software_hive_regback_path, folder_path, partition_start, outfile):
	print("Running Regtime.pl against the registry hives", end = "\n\n")

	if(system_hive_path != "NONE"):	
		#setup system_hive command		
		system_hive_command = "perl /usr/share/windows-perl/regtime.pl -m HKLM-SYSTEM_" + partition_start + " -r " + system_hive_path + " >> " + folder_path + "/bodyfile_" + partition_start
		print("Running Regtime.pl against: " + system_hive_path)
		print("The system_hive_command is: " + system_hive_command, end = "\n\n")
		if(outfile != "NONE"):
			outfile.write("The system_hive_command is: " + system_hive_command + "\n")
			outfile.write("Running Regtime.pl against: " + system_hive_path + "\n\n")
		#run the regtime command
		subprocess.call([system_hive_command], shell=True)

	if(system_hive_regback_path != "NONE"):	
		#setup system_hive command		
		system_hive_regback_command = "perl /usr/share/windows-perl/regtime.pl -m HKLM-SYSTEM_REGBACK_" + partition_start + " -r " + system_hive_regback_path + " >> " + "'" + folder_path + "/bodyfile_" + partition_start + "'"
		print("Running Regtime.pl against: " + system_hive_regback_path)		
		print("The system_hive_regback_command is: " + system_hive_regback_command, end = "\n\n")
		if(outfile != "NONE"):
			outfile.write("The system_hive_regback_command is: " + system_hive_regback_command + "\n")
			outfile.write("Running Regtime.pl against: " + system_hive_regback_path + "\n\n")
		#run the regtime command
		subprocess.call([system_hive_regback_command], shell=True)

	if(sam_hive_regback_path != "NONE"):	
		#setup sam_hive command		
		sam_hive_regback_command = "perl /usr/share/windows-perl/regtime.pl -m HKLM-SAM_REGBACK_" + partition_start + " -r " + sam_hive_regback_path + " >> " + "'" + folder_path + "/bodyfile_" + partition_start + "'"
		print("Running Regtime.pl against: " + sam_hive_regback_path)		
		print("The sam_hive_regback_command is: " + sam_hive_regback_command, end = "\n\n")
		if(outfile != "NONE"):
			outfile.write("The sam_hive_regback_command is: " + sam_hive_regback_command +"\n")
			outfile.write("Running Regtime.pl against: " + sam_hive_regback_path + "\n\n")
		#run the regtime command
		subprocess.call([sam_hive_regback_command], shell=True)

	if(sam_hive_path != "NONE"):	
		#setup sam_hive command		
		sam_hive_command = "perl /usr/share/windows-perl/regtime.pl -m HKLM-SAM_" + partition_start + " -r " + sam_hive_path + " >> " + "'" + folder_path + "/bodyfile_" + partition_start + "'"
		print("Running Regtime.pl against: " + sam_hive_path)		
		print("The sam_hive_command is: " + sam_hive_command, end = "\n\n")
		if(outfile != "NONE"):
			outfile.write("The sam_hive_command is: " + sam_hive_command + "\n")
			outfile.write("Running Regtime.pl against: " + sam_hive_path + "\n\n")
		#run the regtime command
		subprocess.call([sam_hive_command], shell=True)

	if(security_hive_path != "NONE"):	
		#setup security_hive command		
		security_hive_command = "perl /usr/share/windows-perl/regtime.pl -m HKLM-SECURITY_" + partition_start + " -r " + security_hive_path + " >> " + "'" + folder_path + "/bodyfile_" + partition_start + "'"
		print("Running Regtime.pl against: " + security_hive_path )		
		print("The security_hive_command is: " + security_hive_command, end = "\n\n")
		if(outfile != "NONE"):
			outfile.write("The security_hive_command is: " + security_hive_command + "\n")
			outfile.write("Running Regtime.pl against: " + security_hive_path + "\n\n")
		#run the regtime command
		subprocess.call([security_hive_command], shell=True)
	
	if(security_hive_regback_path != "NONE"):	
		#setup security_hive command		
		security_hive_regback_command = "perl /usr/share/windows-perl/regtime.pl -m HKLM-SECURITY_REGBACK_" + partition_start + " -r " + security_hive_regback_path + " >> " + "'" + folder_path + "/bodyfile_" + partition_start + "'"
		print("Running Regtime.pl against: " + security_hive_regback_path)		
		print("The security_hive_regback_command is: " + security_hive_regback_command, end = "\n\n")
		if(outfile != "NONE"):
			outfile.write("The security_hive_regback_command is: " + security_hive_regback_command + "\n\n")
			outfile.write("Running Regtime.pl against: " + security_hive_regback_path + "\n\n")
		#run the regtime command
		subprocess.call([security_hive_regback_command], shell=True)

	if(software_hive_path != "NONE"):	
		#setup software_hive command		
		software_hive_command = "perl /usr/share/windows-perl/regtime.pl -m HKLM-SOFTWARE_" + partition_start + " -r " + software_hive_path + " >> " + "'" + folder_path + "/bodyfile_" + partition_start + "'"
		print("Running Regtime.pl against: " + software_hive_path)		
		print("The software_hive_command is: " + software_hive_command, end = "\n\n")
		if(outfile != "NONE"):
			outfile.write("The software_hive_command is: " + software_hive_command + "\n")
			outfile.write("Running Regtime.pl against: " + software_hive_path + "\n\n")
		#run the regtime"The system_hive_command is: " + system_hive_command, end = "\n\n") command
		subprocess.call([software_hive_command], shell=True)

	if(software_hive_regback_path != "NONE"):	
		#setup software_hive command		
		software_hive_regback_command = "perl /usr/share/windows-perl/regtime.pl -m HKLM-SOFTWARE_REGBACK_" + partition_start + " -r " + software_hive_regback_path + " >> " + "'" + folder_path + "/bodyfile_" + partition_start + "'"
		print("Running Regtime.pl against: " + software_hive_regback_path)		
		print("The software_hive_regback_command is: " + software_hive_regback_command, end = "\n\n")
		if(outfile != "NONE"):
			outfile.write("The software_hive_regback_command is: " + software_hive_regback_command + "\n")
			outfile.write("Running Regtime.pl against: " + software_hive_regback_path + "\n\n")
		#run the regtime command
		subprocess.call([software_hive_regback_command], shell=True)

### REGTIME ##############################################################################

### NTUSER_REGTIME ##############################################################################

def ntuser_regtime(nt_user_dat, folder_path, key, outfile):
	#loop through nt_user_dat list to process each NTUSER.DAT file
	for account in nt_user_dat:
		#get the account profile name
		profile_name = get_account_profile_names(account)
		print("Processing the NTUSER.dat file for User profile: " + str(profile_name))
		if(outfile != "NONE"):
			outfile.write("Processing the NTUSER.dat file for User profile: " + str(profile_name) + "\n")

		#add quotes to image path in case of spaces
		account_quoted = "'" +account +"'"

		#process NTUSER.dat with regtime.pl
		ntuser_command = "perl /usr/share/windows-perl/regtime.pl -m HTLM-USER-" + profile_name + " -r " + account_quoted + " >> " + "'" + folder_path + "/bodyfile_" + key + "'"

		print("the ntuser command is: " + ntuser_command, end = "\n\n")
		if(outfile != "NONE"):
			outfile.write("the ntuser command is: " + ntuser_command + "\n\n")
		subprocess.call([ntuser_command], shell=True)


### NTUSER_REGTIME #############################################################################


### MACTIME #####################################################################################
def mactime(timezone, offset, outfile, folder_path):

	if(timezone == "NONE"):
		#run mactime for data in this partition
		mactime_command = "mactime -d -b " + "'" + folder_path + "/bodyfile_" + str(offset) + "'" +" -z UTC"+ " > " + "'" + folder_path + "/bodyfile_" + str(offset) + "_mactime" + "'"	
	else:
		#run mactime for data in this partition
		mactime_command = "mactime -d -b " + "'" + folder_path + "/bodyfile_" + str(offset) + "'" +" -z " + timezone + " > " + "'" + folder_path + "/bodyfile_" + str(offset) + "_mactime" + "'"
	
	#print out command and then run it
	print("The mactime command is: " + mactime_command)
	if(outfile != "NONE"):
		outfile.write("The mactime command is: " + mactime_command + "\n\n")
	subprocess.call([mactime_command], shell=True)
### MACTIME #####################################################################################

### PROCESS FOLDER ##############################################################################

def process_folder(folder_to_process, folder_path, outfile, case_number, user_defined_timezone):

	#run log2timeline against every file in folder
	if(user_defined_timezone == "NONE"):
		log2timeline_command = "perl /usr/share/log2timeline/log2timeline_legacy -v -o mactime -m Folder -r " + "'" + folder_to_process + "'" + " -log " + "'" + folder_path +"/bodyfile_log2timeline_log.txt" + "'" +" -d -w " + "'" + folder_path +"/bodyfile.txt" + "'"
	else:
		log2timeline_command = "perl /usr/share/log2timeline/log2timeline_legacy -v -z " + user_defined_timezone + " -o mactime -m Folder -r " + "'" + folder_to_process + "'" + " -log " + "'" + folder_path +"/bodyfile_log2timeline_log.txt" + "'" +" -d -w " + "'" + folder_path +"/bodyfile.txt" + "'"
	print ("The log2timeline command is: " + log2timeline_command, end ="\n\n")
	print ("Running Log2timeline against: " + folder_to_process, end ="\n\n")
	subprocess.call([log2timeline_command], shell=True)
	if(outfile != "NONE"):
		outfile.write("The log2timeline command is: " + log2timeline_command + "\n\n")

	#run mac-robber against folder
	macrobber_command = "mac-robber " + "'" + folder_to_process + "'" + " >>" + "'" + folder_path + "/bodyfile.txt" + "'"
	print("The mac-robber command is: " + macrobber_command)
	outfile.write("The macrobber command is: " + macrobber_command + "\n")
	subprocess.call([macrobber_command], shell=True) 

	#run mactime against folder to sort timeline
	if(user_defined_timezone == "NONE"):
		mactime_command = "mactime -d -b " + "'" + folder_path + "/bodyfile.txt" + "'" + "> " + "'" + folder_path + "/" + case_number + "_timeline.csv" + "'"
	else:
		mactime_command = "mactime -d -z " + user_defined_timezone + " -b " + "'" + folder_path + "/bodyfile.txt" + "'" + "> " + "'" + folder_path + "/" + case_number + "_timeline.csv" + "'"
	print("Running mactime against bodyfile")
	subprocess.call([mactime_command], shell=True)

	#run parse timeline module to add extra column
	parse_timeline_module(folder_path, case_number, outfile)

##################################################################################################

### PROCESS FOLDER PLASO ##############################################################################

def plaso_process_folder(Image_Path, folder_path, outfile, case_number, user_defined_timezone, plaso_output_options, cores_to_use):
	
	#convert cores_to_use to string
	#If it fails to convert (for some reason) it will reset the value of corses to use to 1
	try:
		cores_to_use_str = str(cores_to_use)
	except:
		print("Error converting processor cores to string. Reverting to default value of 1 core for processing.")
		if(outfile != "NONE"):
			outfile.write("PLASO DIRECTORY PARSER: Error converting processor cores to string. Reverting to default value of 1 core for processing.")
		cores_to_use_str = "1"
	
	#set plaso command
	if(user_defined_timezone == "NONE"):
		plaso_command = "log2timeline.py --workers " + cores_to_use_str + " -t '" + case_number + "' -z UTC -p --logfile '" + folder_path + "/Timeline_Logs/plaso_logfile.txt' '" + folder_path +"/plaso_timeline.dmp" + "'" +" " + Image_Path + ""
	else:
		plaso_command = "log2timeline.py --workers " + cores_to_use_str + " -t '" + case_number + "' -z " + user_defined_timezone + " --logfile '" + folder_path + "/Timeline_Logs/plaso_logfile.txt' '" + folder_path +"/plaso_timeline.dmp" + "'" +" " + Image_Path + ""
	print ("The Plaso command is: " + plaso_command, end ="\n\n")
	print ("Running Plaso against: " + Image_Path, end ="\n\n")
	if(outfile != "NONE"):
		outfile.write("The plaso command is: " + plaso_command + "\n\n")

	#run the plaso command
	subprocess.call([plaso_command], shell=True)

	#set & run pinfo command
	pinfo_cmd = "pinfo.py -v " + folder_path + "/plaso_timeline.dmp > " + folder_path + "/pinfo_plaso_timeline.txt"
	print ("The Plaso Pinfo command is: " + pinfo_cmd + "\n\n")
	if(outfile != "NONE"):
		outfile.write("The Plaso Pinfo command is: " + pinfo_cmd + "\n\n")
	subprocess.call([pinfo_cmd], shell=True)

	#setup psort options
	
	
	plaso_output_options = plaso_output_options.strip()
	plaso_output_options_split = plaso_output_options.split(",")

	plaso_output_options_split_len = len(plaso_output_options_split)
	print("plaso_output_options = ", plaso_output_options_split_len)

	run_l2tcsv = "False"
	run_sqlite = "False"
	run_elastic = "False"

	check_plaso_output = 0
	while check_plaso_output != plaso_output_options_split_len:
		print("Check_plaso_output is: " + check_plaso_output) 
		print(plaso_output_options_split[check_plaso_output])
		if plaso_output_options_split[check_plaso_output] == "CSV":
			print("l2tcsv ", plaso_output_options_split)
			run_l2tcsv = "True"
			check_plaso_output += 1
		elif plaso_output_options_split[check_plaso_output] == "SQLite":
			print("SQLite ", plaso_output_options_split)
			run_sqlite = "True"
			check_plaso_output += 1
		elif plaso_output_options_split[check_plaso_output] == "Elastic":
			print("Elastic ", plaso_output_options_split)
			run_elastic = "True"
			check_plaso_output += 1
		else:
			print("all ", plaso_output_options_split)
			run_l2tcsv = "False"
			run_sqlite = "False"
			run_elastic = "False"
			check_plaso_output += 1

	if run_l2tcsv == "False" and run_sqlite == "False" and run_elastic == "False":
		print("No output type selected for plaso, saving dump file")



	#set & run psort csv command
	if run_l2tcsv == "True":
		psort_cmd = "psort.py -o L2tcsv -z " +  timezone_shift + " -w " + folder_path + "/plaso_timeline.csv " + folder_path + "/plaso_timeline.dmp"
		print ("The Plaso Psort command is: " + psort_cmd + "\n\n")
		if(outfile != "NONE"):
			outfile.write("The Plaso Psort command is: " + psort_cmd + "\n\n")
		subprocess.call([psort_cmd], shell=True)

	#set & run psort sqlite command
	if run_sqlite == "True":
		psort_cmd = "psort.py -o Sql4n6 -z " + timezone_shift + " -w " + folder_path + "/plaso_sqlite " + folder_path + "/plaso_timeline.dmp"
		print ("The Plaso Psort command is: " + psort_cmd + "\n\n")
		if(outfile != "NONE"):
			outfile.write("The Plaso Psort command is: " + psort_cmd + "\n\n")
		subprocess.call([psort_cmd], shell=True)

	#set & run psort Dynamic command
	if run_elastic == "True":
		psort_cmd = "psort.py -o Dynamic -z " + timezone_shift + " -w '" + folder_path + "/plaso_timeline_dynamic.csv' '" + folder_path + "/plaso_timeline.dmp'"
		print ("The Plaso Psort command is: " + psort_cmd + "\n\n")
		if(outfile != "NONE"):
			outfile.write("The Plaso Psort command is: " + psort_cmd + "\n\n")
		subprocess.call([psort_cmd], shell=True)

### PROCESS FOLDER PLASO ###############################################################################################

### MAIN PROGRAM #####################################################################

def GUI_Timeline_mr(item_to_process, case_number, root_folder_path, evidence, user_defined_timezone, super_timeline_options, plaso_output_options, plaso_processor):
	print("The item to process is: " + item_to_process)
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)
	print("The plaso_output_options are: " + plaso_output_options)

	evidence_no_quotes = evidence
	evidence = '"' + evidence + '"'

	#get datetime
	now = datetime.datetime.now()
	temp_time_wc = now.strftime("%Y-%m-%d_%H_%M_%S_%f")

	#set Mount Point
	mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")
	
	#create output folder path
	folder_path = root_folder_path + "/" + "SuperTimeline"
	check_for_folder(folder_path, "NONE")
	
	#Create log subdirectory
	log_folder_path = folder_path + "/Timeline_Logs"
	check_for_folder(log_folder_path, "NONE")
	
	#open a log file for output
	log_file = log_folder_path + "/SuperTimeline_logfile.txt"
	outfile = open(log_file, 'wt+')



	### INITIALIZE VARIABLES ######
   
	timezone = "NONE"    

	system_hive_path = ""
	system_hive_regback_path = ""
	sam_hive_path = ""
	sam_hive_regback_path = ""
	software_hive_path = ""
	software_hive_regback_path = ""
	security_hive_path = ""
	security_hive_regback_path = ""    
	partition_info_dict = {}

	timezones = []
	timezones_adjusted =[]
	timezone_shift = ""
	partition_hive_path = {}
	### INITIALIZE VARIABLES ######

	super_timeline_options = super_timeline_options.strip()
	super_timeline_options_split = super_timeline_options.split(",")

	super_timeline_options_split_len = len(super_timeline_options_split)
	print("super_timeline_options = ", super_timeline_options_split_len)

	run_l2t = "False"
	run_plaso = "False"

	check_super_timeline = 0
	while check_super_timeline != super_timeline_options_split_len: 
		if super_timeline_options_split[check_super_timeline] == "Log2Timeline":
			print("l2t ", super_timeline_options_split)
			run_l2t = "True"
			check_super_timeline += 1
		elif super_timeline_options_split[check_super_timeline] == "Plaso":
			print("plaso ", super_timeline_options_split)
			run_plaso = "True"
			check_super_timeline += 1
		else:
			print("all ", super_timeline_options_split)
			run_l2t = "False"
			run_plaso = "False"
			check_super_timeline += 1

	if run_l2t == "False" and run_plaso == "False":
		print("No Timeline Tool Selected. Exiting Now")
		sys.exit(0)

	if run_plaso == "True":
		#Calculate Processors for Plaso
		#speed = plaso_processor
		#speed = speed.strip()

		#calculate number of processors to use (Speed-Slow, Speed-Fast, Speed-Med
		calc_cores_command = "cat /proc/cpuinfo | grep processor | wc -l"
		num_of_cores = subprocess.check_output([calc_cores_command], shell=True)
		num_of_cores = num_of_cores.decode(encoding='UTF-8')
		num_of_cores = num_of_cores.strip()
		print("This VM has " + str(num_of_cores) +" cores")

		if(num_of_cores == "1"):
			cores_to_use = 1	
		elif(speed == "Speed-Slow"):
			cores_to_use = 1
		elif(speed == "Speed-Med"):
			cores_to_use = int(num_of_cores)//2
		elif(speed == "Speed-Fast"):
			cores_to_use = int(num_of_cores) - 1

		print("Cores to used is set to: %r" % cores_to_use)

	if(item_to_process == "Directory"):
		print("We are processing a folder")
		#folder_to_process = select_folder_to_process(outfile)
		folder_to_process = evidence_no_quotes
		if run_l2t == "True":
			process_folder(folder_to_process, folder_path, outfile, case_number, user_defined_timezone)
			tool = "l2t"
			split_csv(case_number, temp_time_wc, folder_path, outfile,"l2t")
		if run_plaso == "True":
			plaso_process_folder(folder_to_process, folder_path, outfile, case_number, user_defined_timezone, plaso_output_options, cores_to_use)
			tool = "plaso"
			split_csv(case_number, temp_time_wc, folder_path, outfile, "plaso")
		outfile.close()
	elif(item_to_process =="EnCase Logical Evidence File"):
		#file_to_process = select_file_to_process(outfile)
		file_to_process = evidence_no_quotes
		mount_point = mount_encase_v6_l01(case_number, file_to_process, outfile)
		if run_l2t == "True":
			process_folder(file_to_process, folder_path, outfile, case_number, user_defined_timezone)
			tool = "l2t"
			split_csv(case_number, temp_time_wc, folder_path, outfile, "l2t")
		if run_plaso == "True":
			plaso_process_folder(file_to_process, folder_path, outfile, case_number, user_defined_timezone, plaso_output_options, cores_to_use)
			tool = "plaso"
			split_csv(case_number, temp_time_wc, folder_path, outfile, "plaso")
		outfile.close()

		#umount
		if(os.path.exists(mount_point)):
			subprocess.call(['sudo umount -f ' + mount_point], shell=True)
			os.rmdir(mount_point)
	elif(item_to_process =="Bit-Stream Image"):
		#select dd image to process	
		#Image_Path = select_file_to_process(outfile)
		Image_Path = evidence

		#check if Image file is in Encase format
		if re.search(".E01", Image_Path):
			#strip out single quotes from the quoted path
			#no_quotes_path = Image_Path.replace("'","")
			#print("THe no quotes path is: " +  no_quotes_path)
			#call mount_ewf function
			cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false"
			try:
				subprocess.call([cmd_false], shell=True)
			except:
				print("Autmount false failed")
			Image_Path = mount_ewf(Image_Path, outfile, mount_point)

		#call mmls function
		partition_info_dict, temp_time = mmls(outfile, Image_Path)
		#partition_info_dict_temp, temp_time = partition_info_dict

		#get filesize of mmls_output.txt
		file_size = os.path.getsize("/tmp/mmls_output_" + temp_time + ".txt") 

		#if filesize of mmls output is 0 then run parted
		if(file_size == 0):
			print("mmls output was empty, running parted")
			outfile.write("mmls output was empty, running parted")
			#call parted function
			partition_info_dict, temp_time = parted(outfile, Image_Path)
			#folder_process = select_folder_to_process(outfile)	

		else:

			#read through the mmls output and look for GUID Partition Tables (used on MACS)
			mmls_output_file = open("/tmp/mmls_output_" + temp_time + ".txt", 'r')
			for line in mmls_output_file:
				if re.search("GUID Partition Table", line) or re.search("MAC Partition Map", line):
					print("We found a GUID partition table, need to use parted")
					outfile.write("We found a GUID partition table, need to use parted\n")
					#call parted function
					partition_info_dict, temp_time = parted(outfile, Image_Path)

			#close file
			mmls_output_file.close()

		#loop through dictionary and print out contents to make sure they are sorted
		for key,value in sorted(partition_info_dict.items()):
			print("The offset is: " + str(key) + ". The filesystem is: " + value)
		for key,value in sorted(partition_info_dict.items()):

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
		
				print("We just mounted filesystem: " + value + " at offset:" + str(key) + ". Looking for timezone\n")
				outfile.write("We just mounted filesystem: " + value + " at offset:" + str(key))

				if(user_defined_timezone == "NONE"):
					#get the timezone(s)
					if (value == "hfs+") or (value == "hfs"):
						partition_timezone_final = get_timezones_non_windows(value, system_hive_path, outfile, mount_point)
						timezones.append(str(partition_timezone_final))
						print("Adding timezone: " + str(partition_timezone_final)  + " to the timezone list\n")
						outfile.write("Adding timezone: " + str(partition_timezone_final)  + " to the timezone list\n")
					elif (value == "ext"):
						partition_timezone_final = get_timezones_non_windows(value, system_hive_path, outfile, mount_point)
						timezones.append(str(partition_timezone_final))
						print("Adding timezone: " + str(partition_timezone_final)  + " to the timezone list\n")
						outfile.write("Adding timezone: " + str(partition_timezone_final)  + " to the timezone list\n")
					elif (value == "ntfs" or value == "fat32"):
						#get the system paths for the registry files which you need to find the timezone 
						paths = get_system_paths(value, "NO", outfile, mount_point)

						#set up path variables from paths list
						system_hive_path = paths[0]
						system_hive_regback_path = paths[1]
						sam_hive_path = paths[2]
						sam_hive_regback_path = paths[3]
						software_hive_path = paths[4]
						software_hive_regback_path = paths[5]
						security_hive_path = paths[6]
						security_hive_regback_path = paths[7] 
		
	
						#if the partition has a system hive registry file get the timezone
						if(os.path.isfile(system_hive_path)):
							partition_timezone_final = get_timezones_windows(value, system_hive_path, outfile) 
							timezones.append(str(partition_timezone_final))
							#might need to convert partition_timezone_final to string in the two lines below - more testing needed
							print("Adding timezone: " + str(partition_timezone_final)  + " to the timezone list\n")
							outfile.write("Adding timezone: " + str(partition_timezone_final)  + " to the timezone list\n")
						else:
							#set timezone_final to none
							timezone_final = "NONE"
							timezones.append(timezone_final)
							print("Adding timezone: " + timezone_final  + " to the timezone list\n")
							outfile.write("Adding timezone: " + timezone_final  + " to the timezone list\n")
							print("This partition that starts at sector: " + str(key) + "has no timezone")
							outfile.write("This partition that starts at sector: " + str(key) + "has no timezone\n")

					else:
						#handle fat16 and other partitions without timezones
						#set timezone_final to none
						timezone_final = "NONE"
						timezones.append(timezone_final)
						print("Adding timezone: " + timezone_final  + " to the timezone list\n")
						outfile.write("Adding timezone: " + timezone_final  + " to the timezone list\n")
						print("This partition that starts at sector: " + str(key) + "has no timezone")
						outfile.write("This partition that starts at sector: " + str(key) + "has no timezone\n")
				else:
					#set timezone variable to whatever was manually entered by user
					if(user_defined_timezone != "NONE"):
						timezones.append(user_defined_timezone)

				#unmount and remove mount points
				if(os.path.exists(mount_point)): 
					subprocess.call(['sudo umount -f ' + mount_point], shell=True)
					#os.rmdir(mount_point)
				#unmount loopback device if this image was HFS+ - need to run losetup -d <loop_device> before unmounting
				if not (loopback_device_mount == "NONE"):
					losetup_d_command = "losetup -d " + loopback_device_mount
					subprocess.call([losetup_d_command], shell=True)
			#print out the timezones in the list to determine which one is primary
			for line in timezones:
				if(line != 1):
					print("Timezone in timezone list is: " + line)
					outfile.write("Timezone in timezone list is: " + line + "\n\n")
				else:
					print("This partition has no timezone\n\n")
	

		#after we loop through the dictionary holding the partition information in order to grab the timezone
		#from each parition (if it exists) we now need to determine which timezone to use for paritions that
		#don't have a timezone (data partitions)

		#determine how many timezones are in this image file
		num_timezones = len(timezones)
		print("There are: " + str(num_timezones) + " timezones in this image")
		outfile.write("There are: " + str(num_timezones) + " timezones in this image\n")

		#grab the first valid timezone.  The assumption is that the first valide timezone
		# will be for the C drive.  Use this timezone for any other partition
		#without a timezone


		#set timezone_primary to none
		timezone_primary = "NONE" 

		for i in range(len(timezones)):
			if(timezones[i] != "NONE"):
				timezone_primary = timezones[i]
				#break after we find the first timezone		
				break

		for i in range(len(timezones)):
			if(timezones[i] == "NONE"):
				timezones_adjusted.insert(i, timezone_primary)
				print("adding timezone: "  + timezones[i] + " to position: " + str(i))
			else:
				timezone_primary = timezones[i]
				timezones_adjusted.insert(i, timezone_primary)
				print("adding timezone: "  + timezones[i] + " to position: " + str(i))

		#loop through the timezones_adjusted list to see what the timezones are that we are going to use
		for element in timezones_adjusted:
			print ("The timezone_adjusted timezone is: " + element)
			outfile.write("The timezone_adjusted timezone is: " + element + "\n")

		#setup unmount command
		#unmount_command = "umount -f " + mount_point
		#subprocess.call([unmount_command], shell=True)

		#loop through the dictionary containing the partition info a second time
		#this time we will process the partitions
		#create a counter to use with the timezonex_adjusted list to determine which item to retreive
		counter = 0

		for key,value in sorted(partition_info_dict.items()):
	
			cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false"
			try:
				subprocess.call([cmd_false], shell=True)
			except:
				print("Autmount false failed")
			#call mount sub-routine
			success_code, loopback_device_mount = mount(value,str(key),Image_Path, outfile, mount_point)

			if(success_code):
				print("Could not mount partition with filesystem: " + str(key) + " at offset:" + value)
				outfile.write("Could not mount partition with filesystem: " + str(key) + " at offset:" + value)
			else:
		
				print("We just mounted filesystem: " + value + " at offset:" + str(key))
				outfile.write("We just mounted filesystem: " + value + " at offset:" + str(key))

				#grab the timezone from @timezones_adjusted
				timezone_final = timezones_adjusted.pop()
	
				#print out data 
				print("This filesystem is formatted: " + value)
				print("This filesystem begins at offset: " +  str(key))
				print("The timezone for this partition is: " + timezone_final + "\n\n")

				outfile.write("This filesystem is formatted: " + value + "\n")
				outfile.write("This filesystem begins at offset: " +  str(key) + "\n")
				outfile.write("The timezone for this partition is: " + timezone_final + "\n\n")

				#call plaso
				#print("plaso is: ", run_plaso)
				if run_plaso == "True":
					key_512 = int(key) / 512
					key_512 = int(key_512)
					plaso(str(key_512), folder_path, outfile, Image_Path, timezone_final, plaso_output_options, case_number, cores_to_use)

				#call log2timeline (timezone_shift, offset, folder_path, filesystem)
				#print("l2t is: ", run_l2t)
				if run_l2t == "True":
					log2timeline(timezone_final, str(key), folder_path, outfile, mount_point)
				#if(value.lower() != "ext4"):
				#call fls (offset, folder_path, filesystem) against non NTFS partitions.  Also fls can't support ext4
				#log2timeline will parse the MFT for NTFS partitions
					fls(str(key), folder_path, value, outfile, Image_Path, timezone_final)

				#run mactime command against all fileystem types, pass timezone, offset and list containing begin and end dates
					mactime(timezone_final, key, outfile, folder_path)
	
				#unmount and remove mount points
				if(os.path.exists(mount_point)): 
					subprocess.call(['sudo umount -f ' + mount_point], shell=True)
					os.rmdir(mount_point)
				#unmount loopback device if this image was HFS+ - need to run losetup -d <loop_device> before unmounting
				if not (loopback_device_mount == "NONE"):
					losetup_d_command = "losetup -d " + loopback_device_mount
					subprocess.call([losetup_d_command], shell=True)

		#concatenate output files from mactime and insert header line into CSV file
		#change directory into the cases folder
		os.chdir(folder_path)

		if(run_l2t == "True"):

			#concatenate the body files
			cat_command = "cat *_mactime > " + "'" + folder_path + "/bodyfile_final_temp" + "'"
			#cat_command_tln = "cat *_TLN > " + "'" + folder_path + "/bodyfile_final_TLN" + "'"
			print("The cat command is: " + cat_command)
			#print("The cat_command_tln is: " + cat_command_tln)
			outfile.write("The cat command is: " + cat_command + "\n")
			#outfile.write("The cat command is: " + cat_command_tln + "\n")
			subprocess.call([cat_command], shell=True)
			#subprocess.call([cat_command_tln], shell=True)



			#get length of partition_info_dict to figure out how many bodyfiles there were
			#if there were more than one then you need to add a header to the concatenated final bodyfile
			partition_info_dict_len = len(partition_info_dict)

			if(partition_info_dict_len > 1):
				#grep out the header rows
				grep_command = "grep -Eva Date,Size,Type,Mode bodyfile_final_temp > bodyfile_final"
				subprocess.call([grep_command], shell=True)
	
				#remove the bodyfile_final_temp fit folder to process
				bodyfile_final_temp = folder_path + "/bodyfile_final_temp"
				print("The bodyfile_final_temp is: " + bodyfile_final_temp)
				#bodyfile_final_temp_quoted = "'" +bodyfile_final_temp +"'"	
				os.remove(bodyfile_final_temp)
		
				#set up sort command - this sorts the concatenated bodyfile so that it is in descending order
				sort_command = "sort -k 1.12,1.15 -k 1.5,1.7M -k 1.9,1.10 -k 1.17,1.24 bodyfile_final > " + case_number + "_timeline.csv"
				subprocess.call([sort_command], shell=True)

				#insert header line back into final .csv file
				sed_command = "sed -i '1i\ Date,Size,Type,Mode,UID,GID,Meta,File_Name' " + case_number + "_timeline.csv";
				subprocess.call([sed_command], shell=True)
		
			else: 
				print("No need to sort the final bodyfile since there is only one partition.")
				outfile.write("No need to sort the final bodyfile since there is only one partition.\n\n")
				os.rename('bodyfile_final_temp', case_number + "_timeline.csv")

			#call parse_timeline module to add column into mactime formatted .csv that contains the log2timeline module informaiton
			parse_timeline_module(folder_path, case_number, outfile)
			split_csv(case_number, temp_time_wc, folder_path, outfile, "l2t")

		elif(run_plaso == "True") and (plaso_output_options == "CSV"):

			#get length of partition_info_dict to figure out how many bodyfiles there were
			#if there were more than one then you need to add a header to the concatenated final bodyfile
			partition_info_dict_len = len(partition_info_dict)

			if(partition_info_dict_len > 1):

				#concatenate the .csv files
				cat_command = "cat *.csv > " + "'" + folder_path + "/plaso_timeline_combined.csv" + "'"
				print("The cat command is: " + cat_command)
				outfile.write("The cat command is: " + cat_command + "\n")
				subprocess.call([cat_command], shell=True)

				#grep out the header rows
				grep_command = "grep -Eva date,time,timezone plaso_timeline_combined.csv > plaso_timeline_combined_no_header.csv"
				subprocess.call([grep_command], shell=True)
		
				#set up sort command - this sorts the concatenated bodyfile so that it is in descending order
				sort_command = "sort -k 1.7,1.10 -k 1.1,1.2 -k 1.4,1.5 -k 2.1,2.2 -k 2.4,2.5 -k 2.7,2.8 plaso_timeline_combined_no_header.csv > " + case_number + "_timeline.csv"
				subprocess.call([sort_command], shell=True)

				#remove the bodyfile_final_temp fit folder to process
				bodyfile_final_temp = folder_path + "/plaso_timeline_combined.csv"
				print("The bodyfile_final_temp is: " + bodyfile_final_temp)
				#bodyfile_final_temp_quoted = "'" +bodyfile_final_temp +"'"	
				os.remove(bodyfile_final_temp)

				#insert header line back into final .csv file
				sed_command = "sed -i '1i\ Date,Time,Timezone,MACB,Source,SourceType,type,User,Host,Short,Desc,Version,FileName,Inode,Notes,Format,Extra' " + case_number + "_timeline.csv";
				subprocess.call([sed_command], shell=True)
		
			else: 
				print("No need to sort the final bodyfile since there is only one partition.")
				outfile.write("No need to sort the final bodyfile since there is only one partition.\n\n")
				#os.rename('bodyfile_final_temp', case_number + "_timeline.csv")
			
			#call parse_timeline module to add column into mactime formatted .csv that contains the log2timeline module informaiton
			#parse_timeline_module(folder_path, case_number, outfile)
			split_csv(case_number, temp_time_wc, folder_path, outfile, "plaso")

		#program cleanup
		if os.path.exists("/tmp/wc_" + temp_time_wc + ".txt"):
			os.remove("/tmp/wc_" + temp_time_wc + ".txt")
		if os.path.exists("/tmp/regp_output_*.txt"):
			os.remove("/tmp/regp_output_*.txt")
		if os.path.exists("/tmp/timeline_partition_info_" + temp_time + ".txt"):
			os.remove("/tmp/timeline_partition_info_" + temp_time + ".txt")
		if os.path.exists("/tmp/mmls_output_" + temp_time +".txt"):
			os.remove("/tmp/mmls_output_" + temp_time + ".txt")
		outfile.close()

	#unmount and remove mount points
	if(os.path.exists(mount_point)):
		os.rmdir(mount_point)
	if(os.path.exists(mount_point+"_ewf")):
		subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
		os.rmdir(mount_point+"_ewf")

	#convert outfile using unix2dos	
	unix2dos_command = "sudo unix2dos " + "'" + log_file + "'"
	print("The unix2dos command is: " + unix2dos_command)
	subprocess.call([unix2dos_command], shell=True)

	#delete /tmp files
	if (os.path.exists("/tmp/regp_output*.txt")):
		os.remove("/tmp/regp_output*.txt")

	#call done sub to tell user program is done and alert them where the output files are located
	#done(folder_path)


### MAIN PROGRAM #####################################################################	
