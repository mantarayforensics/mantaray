#!/usr/bin/env python3
#This program will run bulk_extractor on a file, folder or disk image, or L01

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

import os
from os.path import join
import re
import io
import sys
import string
import subprocess
import pickle
import datetime

### PROCESS FOLDER ##############################################################################

def process_folder(evidence, folder_path_be, whitelist_location, speed, outfile, keyword_list, cores_to_use):

	#set up bulk_extractor command
	if(whitelist_location != "NONE") and (keyword_list == "NONE"):
		be_command = "bulk_extractor -o " + folder_path_be + ' -w "' + whitelist_location + '" -j ' + str(cores_to_use) + " -R " + evidence
	elif(whitelist_location == "NONE") and (keyword_list =="NONE"):
		be_command = "bulk_extractor -o " + folder_path_be + " -j " + str(cores_to_use) + " -R " + evidence
	elif(whitelist_location != "NONE") and (keyword_list != "NONE"):
		be_command = "bulk_extractor -o " + folder_path_be + ' -w "' + whitelist_location + '" -x find -F "' + keyword_list + '" -j ' + str(cores_to_use) + " -R " + evidence
	elif(whitelist_location == "NONE") and (keyword_list != "NONE"):
		be_command = "bulk_extractor -o " + folder_path_be + ' -x find -F "' + keyword_list + '" -j ' + str(cores_to_use) + " -R " + evidence

	#run be_command
	subprocess.call([be_command], shell=True)

#################################################################################################



#GUI_input = []

#at command line enter item_to_process(folder, l01, image), case_name, output_folder, evidence_to_process, whitelist_location, speed
#GUI_input = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]

def be_mr(item_to_process, case_number, folder_path, evidence, whitelist_location, speed, keyword_list):
	evidence = "'" + evidence + "'"
	speed = speed.strip()

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
		cores_to_use = num_of_cores 
	

	print("Item to process is: " + item_to_process)
	print("Case number is: " + case_number)
	print("Output folder is: " + folder_path)
	print("Evidence type is: " + evidence)
	print("Whitelist location is: " + whitelist_location)
	print("Processing speed is: " + speed)
	print("Keyword list is: " + keyword_list)

	#open a log file for output
	#log_file = folder_path + "/" + case_number + "_logfile.txt"
	#outfile = open(log_file, 'a')

	#add subfolder to output path so BE has empty folder to write to
	folder_path_be = "'" + folder_path +"/Bulk_Extractor_Results'" 
	check_for_folder(folder_path_be, "NONE")
	
	if(item_to_process == "Directory"):
		process_folder(evidence, folder_path_be, whitelist_location, speed, "NONE", keyword_list, cores_to_use)
	elif(item_to_process == "EnCase Logical Evidence File"):
		mount_point = mount_encase_v6_l01(case_number, evidence, "NONE")
		process_folder(mount_point, folder_path_be, whitelist_location, speed, "NONE", keyword_list, cores_to_use)
	elif(item_to_process == "Single File") or (item_to_process == "Memory Image") or (item_to_process == "EnCase Logical Evidence File"):

		#set up bulk extractor command
		if(whitelist_location != "NONE") and (keyword_list == "NONE"):
			be_command = "bulk_extractor -o " + folder_path_be + ' -w "' + whitelist_location + '" -j ' + str(cores_to_use) + " " + evidence
		elif(whitelist_location == "NONE") and (keyword_list =="NONE"):
			be_command = "bulk_extractor -o " + folder_path_be + " -j " + str(cores_to_use) + " " + evidence
		elif(whitelist_location != "NONE") and (keyword_list != "NONE"):
			be_command = "bulk_extractor -o " + folder_path_be + ' -w "' + whitelist_location + '" -x find l -F "' + keyword_list + '" -j ' + str(cores_to_use) + " " + evidence
		elif(whitelist_location == "NONE") and (keyword_list != "NONE"):
			be_command = "bulk_extractor -o " + folder_path_be + ' -x find -F "' + keyword_list + '" -j ' + str(cores_to_use) + " " + evidence

		#outfile.write("The be_command is: " + be_command + "\n")

		#run be_command
		print("The be command is: " + be_command)
		subprocess.call([be_command], shell=True)
	elif(item_to_process == "Bit-Stream Image"):
		#set up bulk extractor command
		if(whitelist_location != "NONE") and (keyword_list == "NONE"):
			be_command = "bulk_extractor -C 60 -o " + folder_path_be + ' -w "' + whitelist_location + '" -j ' + str(cores_to_use) + " " + evidence
		elif(whitelist_location == "NONE") and (keyword_list =="NONE"):
			be_command = "bulk_extractor -C 60 -o " + folder_path_be + " -j " + str(cores_to_use) + " " + evidence
		elif(whitelist_location != "NONE") and (keyword_list != "NONE"):
			be_command = "bulk_extractor -C 60 -o " + folder_path_be + ' -w "' + whitelist_location + '" -x find l -F "' + keyword_list + '" -j ' + str(cores_to_use) + " " + evidence
		elif(whitelist_location == "NONE") and (keyword_list != "NONE"):
			be_command = "bulk_extractor -C 60 -o " + folder_path_be + ' -x find -F "' + keyword_list + '" -j ' + str(cores_to_use) + " " + evidence

		#run be_command
		print("The be command is: " + be_command)
		subprocess.call([be_command], shell=True)

		#run fiwalk
		fiwalk_command = "fiwalk -x " + evidence + " >" + '"' + folder_path + "/Bulk_Extractor_Results/fiwalk_output.xml" + "'"
		print("Running fiwalk: " + fiwalk_command)
		subprocess.call([fiwalk_command], shell=True)

		#run identify_filenames.py
		identify_filenames_command = "python3 /usr/share/bulk_extractor/python/identify_filenames.py --all --imagefile " + evidence + " --xmlfile " + '"' + folder_path + "/Bulk_Extractor_Results/fiwalk_output.xml" + '"' + " "  + '"' + folder_path + "/Bulk_Extractor_Results" + '"' + " " + '"' + folder_path + "/Bulk_Extractor_Results/annotated_results/" + '"'
		print("Running identify_filenames.py: " + identify_filenames_command)
		subprocess.call([identify_filenames_command], shell=True)

		#chdir to output foler
		os.chdir(folder_path)

		#run text files through unix2dos
		for root, dirs, files in os.walk(folder_path + "/Bulk_Extractor_Results/"):
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

