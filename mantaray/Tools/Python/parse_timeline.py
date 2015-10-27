#parse the final .csv file output from supertimeline script

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2013 dougkoster@hotmail.com				                 #
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


#get file to process
csv_file = fileopenbox(msg="Select File to Process",title="Select File",default='/mnt/hgfs/*.*')

#get output folder
folder_path = diropenbox(msg="Output Location",title="Choose Path",default='/mnt/hgfs/')

#open csv file
infile = open(csv_file, encoding='latin-1')
#infile = open(csv_file, 'r+')

#open outfile
out_file = csv_file + "_timeline_modules.csv"
outfile = open(out_file, 'wt+')

#skip header row
next(infile)

#loop through csv file
for line in infile:
	#split line on space
	#line_split = line.split(',')
	line_split = line.split(",",7)


	date_time = line_split[0]
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
		#print(line)

		#determine log2timeline module
		module_name = file_name.split(']')
		module_name1 = module_name[0].replace('[','')
		module_name1 = module_name[0].replace('"','')
		print("The module is: " + module_name1 + "]")

		#create new line for output file
		newline = date_time + ',' + size + "," + type1 + ',' + mode + ',' + uid + ',' + gid + ',' + meta + ',' + module_name1 + '],' + file_name
		outfile.write(newline)
		
	else:
		newline = date_time + ',' + size + "," + type1 + ',' + mode + ',' + uid + ',' + gid + ',' + meta + ',' +'' + ',' + file_name
		print("The module is: N/A")		
		outfile.write(newline)
outfile.close()

#add header line back into modified supertimeline
sed_command = "sudo sed -i '1i\ Date,Size,Type,Mode,UID,GID,Meta,L2T_Function,File_Name' "  + "'"+ csv_file +"_timeline_modules.csv" + "'";
subprocess.call([sed_command], shell=True)
	
