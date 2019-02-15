#!/usr/bin/env python3
#This program parses a PST file and searches for email addresses of interest 
#supplied by the user

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2018 dougkoster@hotmail.com				                 #
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
from split_csv import *

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

def process_folder(folder_path, case_number, evidence, outfile, plaso_options):

	#run plaso to create dump file

	#set up plaso command
	plaso_command = "log2timeline.py " + "'" + folder_path + "/" + case_number + ".dump" + "'" + " " + "'" + evidence + "'" +  " --partition all --status_view window --logfile " + "'" + folder_path + "/" + case_number + "_plaso.log" + "'" + " --vss-stores all"
	print("The plaso command is: " + plaso_command)
	#run plaso command
	subprocess.call([plaso_command], shell=True)

	if ("CSV" in plaso_options):

		#set up psort command
		psort_command = "psort.py --logfile " + "'" + folder_path + "/" + case_number + "_pysort.log" + "'" + " -w " + "'" + folder_path + "/" + case_number + ".plaso.csv" + "'" + " -o l2tcsv " + "'" + folder_path + "/" + case_number + ".dump" + "'"
		print("The psort command is: " + psort_command)
		outfile.write("The psort command is: " + psort_command + "\n")

		#run psort command
		subprocess.call([psort_command], shell=True)

	if ("Kibana" in plaso_options):

		#set up psort command
		#psort.py -o elastic --index_name case-test --raw_fields test-plaso.dump
		psort_command = "psort.py -o elastic --index_name " + case_number + " --raw_fields --logfile " + "'" + folder_path + "/" + case_number + "_pysort.log" + "'" +" " +  "'" + folder_path + "/" + case_number + ".dump" + "'"
		print("The psort command is: " + psort_command)
		outfile.write("The psort command is: " + psort_command + "\n")

		#run psort command
		subprocess.call([psort_command], shell=True)


	if ("Timesketch" in plaso_options):

		#set up psort command
		psort_command = "psort.py -o timesketch --name " + case_number + " --index " + case_number + " --logfile " + "'" + folder_path + "/" + case_number + "_pysort.log" + "'" +" " +  "'" + folder_path + "/" + case_number + ".dump" + "'"
		print("The psort command is: " + psort_command)
		outfile.write("The psort command is: " + psort_command + "\n")

		#run psort command
		subprocess.call([psort_command], shell=True)

##########################################################################################################

##########################################################################################################

def pst_processor_mr(item_to_process, case_number, root_folder_path, evidence):
	#(evidence_type, case_number, folder_path, evidence_path.strip())
	
	print("The item to process is: " + item_to_process)
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)

	evidence_no_quotes = evidence
	evidence = "'" + evidence + "'"

	root_folder_path_no_quotes = root_folder_path
	root_folder_path = "'" + root_folder_path + "'"

	#get datetime
	now = datetime.datetime.now()
	
	#create output folder path
	folder_path = root_folder_path_no_quotes + "/" + "PST_Extracted_Emails"
	check_for_folder(folder_path, "NONE")

	#create folder for extracted_messages
	check_for_folder(folder_path + "/" "All Extracted_Messages", "NONE")
	

	#open a log file for output
	log_file = folder_path + "/PST_mr_logfile.txt"
	outfile = open(log_file, 'wt+')

	emails_of_interest_file = subprocess.check_output(['zenity --file-selection --filename="/mnt/hgfs/" '
										'--title "Select file containing email addresses of interest (comma seperated)"'],
										shell=True, universal_newlines=True)
		
	
	#process the PST file
	process_pst_command = 'readpst -o ' + "'" + folder_path + "/" "All Extracted_Messages" + "'" + " -D -j 4 -r -tea -e " + evidence	
	print("The process_pst_command is: " + process_pst_command)
	subprocess.call([process_pst_command],shell=True, universal_newlines=True)

	#open emails_of_interest_file and parse emails into list
	with open(emails_of_interest_file.strip(), 'r', encoding='utf-8') as infile:
		for line in infile:
			email_addresses_split = line.split(',')
			for element in email_addresses_split:
				print("Creating output folder for email address: " + element)
				check_for_folder(folder_path + "/" + element, "NONE")

				#cd into the extracted_messages SENT folder
				os.chdir(folder_path + "/" "All Extracted_Messages/Personal Folders/Sent Items")

				#run the grep command in the SENT folder
				grep_command = "grep -rl --null --include '*.msg' --include '*.eml' " + element + " | xargs -0r cp -t " + "'" + folder_path + "/" + element + "'"
				print("The grep_command is: " + grep_command)
				subprocess.call([grep_command],shell=True, universal_newlines=True)

	#close output file
	outfile.close()

	
