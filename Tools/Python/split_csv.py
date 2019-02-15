#!/usr/bin/env python3
#This program splits a csv file passed from the supertimeline creation process
#The goal is to split the CSV into multiple smaller csv files that can be opened by EXCEL with a 1M line max

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

def split_csv(case_number, folder_path, outfile, file_to_split, file_to_split_basename):
	
	
	word_count_command = "wc -l " + "'" + file_to_split + "'" + " | awk '{print $1}' > /tmp/wc_" + file_to_split_basename + ".txt"	
	lines = (subprocess.call([word_count_command], shell=True))

	fh = open('/tmp/wc_' + file_to_split_basename + '.txt')

	for line in fh:
		#strip trailing carriage return
		line = line.strip()
		print("The number of lines from the wc command where: " + line)
		
		#since there is only one line in the input file we can now figure out if the file needs to be split
		#if the line has between 1M and 2M lines then divide the number of lines by 2 to determine where to split
		if(int(line) > 1000000) and (int(line) < 2000000):
			print("There are " + str(line) + " in this output file, so it needs to be split")
			outfile.write("There are " + str(line) + " in this output file, so it needs to be split\n\n")
			#figure out what number to use in the split command
			split_number = (int(line)//2) + 1

			#set up the split command
			split_command = "split -l " + str(split_number) + " " + file_to_split
			print ("The split command is: " + split_command)
			outfile.write("The split command is: " + split_command + "\n\n")
			subprocess.call([split_command], shell=True)

			#rename files output from split command
			for root,dirs,files in os.walk(folder_path):
				for filenames in files:
					if re.search("xaa", filenames):
						#the first split file already contains the correct header line so just rename it
						os.rename(filenames, case_number + "_timeline_split_"+filenames+".csv")
					elif re.search("xa", filenames):
						full_path = os.path.join(root, filenames)
						#add header info back into split file
						sed_command = "sed -i '1i\ date,time,timezone,MACB,source,sourcetype,type,user,host,short,desc,version,filename,inode,notes,format,extra' " + "'"+full_path+"'"
						subprocess.call([sed_command], shell=True)
						os.rename(filenames, case_number + "_timeline_modules_split_"+filenames+".csv")			
					

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
			split_command = "split -l " + str(split_number_final) + " " + case_number + "_timeline_modules.csv"
			print ("The split command is: " + split_command)
			outfile.write("The split command is: " + split_command + "\n\n")
			subprocess.call([split_command], shell=True)
			
			#rename files output from split command
			for root,dirs,files in os.walk(folder_path):
				for filenames in files:
					if re.search("xaa", filenames):
						#the first split file already contains the correct header line so just rename it
						os.rename(filenames, case_number + "_timeline_split_"+filenames+".csv")
					elif re.search("xa", filenames):
						full_path = os.path.join(root, filenames)
						#add header info back into split file
						sed_command = "sed -i '1i\ date,time,timezone,MACB,source,sourcetype,type,user,host,short,desc,version,filename,inode,notes,format,extra' " + "'"+full_path+"'"
						subprocess.call([sed_command], shell=True)
						os.rename(filenames, case_number + "_timeline_modules_split_"+filenames+".csv")

		else:
			outfile.write("There are: " + str(line) + " in the supertimeline" + "\n")
			print("There are: " + str(line) + " lines in the supertimeline" + "\n")

	fh.close()
	os.remove('/tmp/wc_' + file_to_split_basename + '.txt')
