#!/usr/bin/env python3
#This program runs static malware analysis tools from remnux
#Your SIFT VM must be merged with REMNUX for this to work
#Please see: https://digital-forensics.sans.org/blog/2015/06/13/how-to-install-sift-workstation-and-remnux-on-the-same-forensics-system
#If you want Mastiff to automatically send your file to VirusTotal you need to insert your VT API key into the file: /etc/mastiff/mastiff.conf

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2015 dougkoster@hotmail.com			                     #
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

def process_folder(folder_to_process, folder_path, evidence_no_quotes, outfile):
	for root,dirs,files in os.walk(folder_to_process):
		for file_name in files:
			print("The current file is: " + file_name)
			abs_file_path = os.path.join(root,file_name)
			quoted_abs_file_path = '"'+abs_file_path+'"'

			file_name_print = file_name.encode('utf-8')
			abs_file_path_print = abs_file_path.encode('utf-8')

			#make output folder for this file
			check_for_folder(folder_path + "/" + file_name, "NONE")

			#clean up printable variables
			file_name_print = re.sub('b\'','',str(file_name_print))
			file_name_print = re.sub("'",'',file_name_print)

			abs_file_path_print = re.sub('b\'','',str(abs_file_path_print))
			abs_file_path_print = re.sub("'",'', abs_file_path_print)

			print("The file to process is: " + abs_file_path_print)
			filename = os.path.basename(abs_file_path)
			run_mastiff("'"+ abs_file_path_print + "'", filename, folder_path, abs_file_path_print, outfile)
			run_pescanner("'"+ abs_file_path_print + "'", filename, folder_path, abs_file_path_print, outfile)
			run_pestr("'"+ abs_file_path_print + "'", filename, folder_path, abs_file_path_print, outfile)
			run_readpe("'"+ abs_file_path_print + "'", filename, folder_path, abs_file_path_print, outfile)
			run_pedump("'"+ abs_file_path_print + "'", filename, folder_path, abs_file_path_print, outfile)
			run_peframe("'"+ abs_file_path_print + "'", filename, folder_path, abs_file_path_print, outfile)
			run_signsrch("'"+ abs_file_path_print + "'", filename, folder_path, abs_file_path_print, outfile)
			

##########################################################################################################

### Run MASTIFF #########################################################################################

def run_mastiff(evidence, file_to_process, folder_path, evidence_no_quotes, outfile):
	print("Getting ready to run Mastiff.....")
	print("The file to process is: " + file_to_process)

	#make output folder for this file
	check_for_folder(folder_path + "/" + file_to_process + "/MASTIFF", "NONE")


	#get md5 hash of file we are processing
	md5_hash = calculate_md5(evidence_no_quotes)
	print("The md5 hash of this file is: " + md5_hash)

	#set up mastiff command
	mastiff_command = "mas.py " + evidence 
	print("The mastiff command is: " + mastiff_command)
	outfile.write("The mastiff command is: " + mastiff_command + "\n\n")

	#run mastiff command
	subprocess.call([mastiff_command], shell=True)

	#move the mastiff output folder to the mantaray output folder
	move_command = "mv /var/log/mastiff/" + md5_hash + " " + "'" + folder_path + "/" + file_to_process + "/MASTIFF" + "'"
	print("The move command is: " + move_command)
	outfile.write("The move command is: " + move_command + "\n\n")
	#run move_command
	subprocess.call([move_command], shell=True)


##########################################################################################################

### Run PESCANNER #########################################################################################

def run_pescanner(evidence, file_to_process, folder_path, evidence_no_quotes, outfile):
	print("Getting ready to run PESCANNER.....")
	print("The file to process is: " + file_to_process)

	#make output folder for this file
	check_for_folder(folder_path + "/" + file_to_process + "/PESCANNER", "NONE")

	#get md5 hash of file we are processing
	#md5_hash = calculate_md5(evidence_no_quotes)
	#print("The md5 hash of this file is: " + md5_hash)

	#set up mastiff command
	pescanner_command = "pescanner.py " + evidence + " > " + "'" + folder_path + "/" + file_to_process + "/PESCANNER/PESCANNER_output.txt" + "'"
	print("The pescanner command is: " + pescanner_command)
	outfile.write("The pescanner command is: " + pescanner_command + "\n\n")

	#run mastiff command
	subprocess.call([pescanner_command], shell=True)


##########################################################################################################

### Run PESTR #########################################################################################

def run_pestr(evidence, file_to_process, folder_path, evidence_no_quotes, outfile):
	print("Getting ready to run PESTR.....")
	print("The file to process is: " + file_to_process)

	#make output folder for this file
	check_for_folder(folder_path + "/" + file_to_process + "/PESTR", "NONE")

	#get md5 hash of file we are processing
	#md5_hash = calculate_md5(evidence_no_quotes)
	#print("The md5 hash of this file is: " + md5_hash)

	#set up mastiff command
	pestr_command = "pestr " + evidence + " > " + "'" + folder_path + "/" + file_to_process + "/PESTR/PESTR_output.txt" + "'"
	print("The pestr command is: " + pestr_command)
	outfile.write("The pestr command is: " + pestr_command + "\n\n")

	#run prestr command
	subprocess.call([pestr_command], shell=True)


##########################################################################################################

### Run READPE #########################################################################################

def run_readpe(evidence, file_to_process, folder_path, evidence_no_quotes, outfile):
	print("Getting ready to run READPE.....")
	print("The file to process is: " + file_to_process)

	#make output folder for this file
	check_for_folder(folder_path + "/" + file_to_process + "/READPE", "NONE")

	#get md5 hash of file we are processing
	#md5_hash = calculate_md5(evidence_no_quotes)
	#print("The md5 hash of this file is: " + md5_hash)

	#set up readpe command
	readpe_command = "readpe " + evidence + " > " + "'" + folder_path + "/" + file_to_process + "/READPE/READPE_output.txt" + "'"
	print("The readpe command is: " + readpe_command)
	outfile.write("The readpe command is: " + readpe_command + "\n\n")

	#run prestr command
	subprocess.call([readpe_command], shell=True)


##########################################################################################################

### Run PEDUMP #########################################################################################

def run_pedump(evidence, file_to_process, folder_path, evidence_no_quotes, outfile):
	print("Getting ready to run PEDUMP.....")
	print("The file to process is: " + file_to_process)

	#make output folder for this file
	check_for_folder(folder_path + "/" + file_to_process + "/PEDUMP", "NONE")

	#get md5 hash of file we are processing
	#md5_hash = calculate_md5(evidence_no_quotes)
	#print("The md5 hash of this file is: " + md5_hash)

	#set up pedump command
	pedump_command = "pedump " + evidence + " > " + "'" + folder_path + "/" + file_to_process + "/PEDUMP/PEDUMP_output.txt" + "'"
	print("The pedump command is: " + pedump_command)
	outfile.write("The pedump command is: " + pedump_command + "\n\n")

	#run pedump command
	subprocess.call([pedump_command], shell=True)

##########################################################################################################

### Run PEDUMP #########################################################################################

def run_peframe(evidence, file_to_process, folder_path, evidence_no_quotes, outfile):
	print("Getting ready to run PEFRAME.....")
	print("The file to process is: " + file_to_process)

	#make output folder for this file
	check_for_folder(folder_path + "/" + file_to_process + "/PEFRAME", "NONE")

	#set up peframe command
	peframe_command = "peframe " + evidence + " > " + "'" + folder_path + "/" + file_to_process + "/PEFRAME/PEFRAME_output.txt" + "'"
	print("The peframe command is: " + peframe_command)
	outfile.write("The peframe command is: " + peframe_command + "\n\n")

	#run peframe command
	subprocess.call([peframe_command], shell=True)

##########################################################################################################

### Run SIGNSRCH #########################################################################################

def run_signsrch(evidence, file_to_process, folder_path, evidence_no_quotes, outfile):
	print("Getting ready to run PEFRAME.....")
	print("The file to process is: " + file_to_process)

	#make output folder for this file
	check_for_folder(folder_path + "/" + file_to_process + "/SIGNSRCH", "NONE")

	#set up signsrch command
	signsrch_command = "signsrch " + evidence + " > " + "'" + folder_path + "/" + file_to_process + "/SIGNSRCH/SIGNSRCH_output.txt" + "'"
	print("The signsrch command is: " + signsrch_command)
	outfile.write("The signsrch command is: " + signsrch_command + "\n\n")

	#run signsrch command
	subprocess.call([signsrch_command], shell=True)

##########################################################################################################




def sa_mr(item_to_process, case_number, root_folder_path, evidence):
	
	print("The item to process is: " + item_to_process)
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)

	evidence_no_quotes = evidence
	evidence = '"' + evidence + '"'

	#get datetime
	now = datetime.datetime.now()

	#set Mount Point
	mount_point = "/mnt/" + "MantaRay_" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")
	
	#create output folder path
	folder_path = root_folder_path + "/" + "Static Malware Analysis"
	check_for_folder(folder_path , "NONE")
	

	#open a log file for output
	log_file = folder_path + "/Static_Malware_Analysis_logfile.txt"
	outfile = open(log_file, 'wt+')

	if(item_to_process == "Single File"):
		#get base filename to process
		filename = os.path.basename(evidence_no_quotes)
		print("The file to process is: " + filename)

		#make output folder for this file
		check_for_folder(folder_path + "/" + filename, "NONE")

		#run Mastiff
		run_mastiff(evidence, filename, folder_path, evidence_no_quotes, outfile)

		#run pescanner
		run_pescanner(evidence, filename, folder_path, evidence_no_quotes, outfile)

		#run pestr
		run_pestr(evidence, filename, folder_path, evidence_no_quotes, outfile)

		#run readpe
		run_readpe(evidence, filename, folder_path, evidence_no_quotes, outfile)

		#run pedump
		run_pedump(evidence, filename, folder_path, evidence_no_quotes, outfile)

		#run peframe
		run_peframe(evidence, filename, folder_path, evidence_no_quotes, outfile)

		#run signsrch
		run_signsrch(evidence, filename, folder_path, evidence_no_quotes, outfile)

	elif(item_to_process == "Directory"):
		folder_to_process = evidence_no_quotes
		#get base filename to process
		process_folder(folder_to_process, folder_path, evidence_no_quotes, outfile)
	elif(item_to_process =="EnCase Logical Evidence File"):
		file_to_process = evidence
		mount_point = mount_encase_v6_l01(case_number, file_to_process, outfile)
		process_folder(mount_point, folder_path, evidence_no_quotes, outfile)

		#umount
		if(os.path.exists(mount_point)):
			subprocess.call(['sudo umount -f ' + mount_point], shell=True)
			os.rmdir(mount_point)


	#remove mount points created for this program
	if(os.path.exists(mount_point)):
		os.rmdir(mount_point)
	if(os.path.exists(mount_point+"_ewf")):
		subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
		os.rmdir(mount_point+"_ewf")

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
				print("Running Unix2dos against file: " + quoted_full_path)
				unix2dos_command = "sudo unix2dos " + quoted_full_path
				subprocess.call([unix2dos_command], shell=True)

