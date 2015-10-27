#parse the final .csv file output from supertimeline script

#import modules
from easygui import *
from timezone_setting import *
from get_case_number import *
from get_output_location import *
from select_file_to_process import *
from parted import *
from mount import *
from mount_ewf import *
from get_ntuser_paths import *
from get_system_paths import *
from done import *
from unix2dos import *
from mmls import *
import os
from os.path import join
import re
import io
import sys
import string
import subprocess

def parse_timeline_module(folder_path, case_number, outfile):

	#changedir into output folder
	os.chdir(folder_path)

	#print input file name
	print("The folder path is: " + folder_path)
	outfile.write("The folder path is: " + folder_path + "\n")
	print("The case_number is: " + case_number)
	outfile.write("The case_number is: " + case_number + "\n")

	#infile
	csv_file = case_number + "_timeline.csv"

	#use tr command to get rid of carriage returns
	tr_command = "cat " + csv_file + " | tr '\r' ' ' > /tmp/parsing_input_file.csv"
	subprocess.call([tr_command], shell=True)

	#open csv file
	infile = open('/tmp/parsing_input_file.csv', encoding='latin-1')

	#open outfile
	out_file = folder_path + "/"+ case_number + "_timeline_modules.csv"
	csv_file_modules = open(out_file, 'wt+')

	#skip header row
	next(infile)
	#loop through input file
	for line in infile:
		#split line on space
		line1 = line.replace('\n', ' ')
		#print(line1)
		line_split = line1.split(',',7)
		date_time = line_split[0]

		#clean up date/time so it is sortable in excel
		if (re.search("Mon ", date_time)):
			date_time_dave = date_time.replace("Mon ","")
		elif (re.search("Tue ", date_time)):
			date_time_dave = date_time.replace("Tue ","")
		elif (re.search("Wed ", date_time)):
			date_time_dave = date_time.replace("Wed ","")
		elif (re.search("Thu ", date_time)):
			date_time_dave = date_time.replace("Thu ","")
		elif (re.search("Fri ", date_time)):
			date_time_dave = date_time.replace("Fri ","")
		elif (re.search("Sat ", date_time)):
			date_time_dave = date_time.replace("Sat ","")
		elif (re.search("Sun ", date_time)):
			date_time_dave = date_time.replace("Sun ","")

		if not (re.search("Xxx", date_time)):
			#convert date/time format
			date_time_dave1 = date_time_dave.replace(" ", "/",2)
			date_time = date_time_dave1

			if (re.search("Jan", date_time)):
				date_time_dave = date_time.replace("Jan", "01")
			elif (re.search("Feb", date_time)):
				date_time_dave = date_time.replace("Feb", "02")
			elif (re.search("Mar", date_time)):
				date_time_dave = date_time.replace("Mar", "03")
			elif (re.search("Apr", date_time)):
				date_time_dave = date_time.replace("Apr", "04")
			elif (re.search("May", date_time)):
				date_time_dave = date_time.replace("May", "05")
			elif (re.search("Jun", date_time)):
				date_time_dave = date_time.replace("Jun", "06")
			elif (re.search("Jul", date_time)):
				date_time_dave = date_time.replace("Jul", "07")
			elif (re.search("Aug", date_time)):
				date_time_dave = date_time.replace("Aug", "08")
			elif (re.search("Sep", date_time)):
				date_time_dave = date_time.replace("Sep", "09")
			elif (re.search("Oct", date_time)):
				date_time_dave = date_time.replace("Oct", "10")
			elif (re.search("Nov", date_time)):
				date_time_dave = date_time.replace("Nov", "11")
			elif (re.search("Dec", date_time)):
				date_time_dave = date_time.replace("Dec", "12")

			date_time = date_time_dave


		size = line_split[1]
		type1 = line_split[2]
		mode = line_split[3]
		uid = line_split[4]
		gid = line_split[5]
		meta = line_split[6]
		file_name = line_split[7]

		#remove " from file_name
		file_name1 = file_name.replace('"', '')

		if(re.search('^\\[', file_name1)):

			#determine log2timeline module
			module_name = file_name.split(']')
			module_name1 = module_name[0].replace('[','')
			module_name1 = module_name[0].replace('"','')
			#print("The module is: " + module_name1 + "]")

			#create new line for output file
			newline = date_time + ',' + size + "," + type1 + ',' + mode + ',' + uid + ',' + gid + ',' + meta + ',' + module_name1 + '],' + file_name
			csv_file_modules.write(newline + '\n')
		
		else:
			newline = date_time + ',' + size + "," + type1 + ',' + mode + ',' + uid + ',' + gid + ',' + meta + ',' +'' + ',' + file_name
			#print("The module is: N/A")		
			csv_file_modules.write(newline + '\n')

	csv_file_modules.close()

	#add header line back into modified supertimeline
	sed_command = "sudo sed -i '1i\ Date,Size,Type,Mode,UID,GID,Meta,L2T_Function,File_Name' "  + "'"+ folder_path + "/" + case_number + "_timeline_modules.csv" + "'"
	outfile.write("The sed command is: " + sed_command + "\n")
	subprocess.call([sed_command], shell=True)
	csv_file_modules.close()
	
	#close file
	infile.close()

	return "'"+ folder_path + "/" + case_number + "_timeline_modules.csv" + "'"
	
