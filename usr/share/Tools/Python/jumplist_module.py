#!/usr/bin/env python3
#Module for FAEB.  Runs j[.pl (Harlan Carvey) against every JumpList file
#OUTPUT: TLN formatted file and timeline file

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2012               					 #
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
from done import *
from unix2dos import *

import os
import re
import io
import sys
import string
import subprocess
import shutil

##### GET ACCOUNT PROFILE NAME ##########################################################################################################################
def get_account_profile_names(account, outfile2):
	#Takes absolute path to Jumplist file and returns the profile name

	print("The account name passed to the function is: " + account)
	outfile.write("The account name passed to the function is: " + account + "\n")

	#get substring
	account_sub = account[:-105]
	outfile.write("The account-sub name passed to the function is: " + account_sub + "\n")


	#get length
	account_sub_string_length = len(account_sub)

	#find offset of rightmost slash
	rightmost_slash_location = account_sub.rindex('/')

	#calculate substring	
	username = account_sub[(rightmost_slash_location+1):account_sub_string_length]

	return username


##### GET ACCOUNT PROFILE NAME ##########################################################################################################################

def jumplist_module(full_path, outfile, folder_path, offset):

	outfile.write("Processing Jump List: " + full_path + "\n")

	#get profile name
	if(offset != "FOLDER"):
		profile = get_account_profile_names(full_path, outfile2)
		print("The profile is: " + profile)
		outfile.write("The profile is: " + profile + "\n")
	else:
		profile = "Unknown-Folder_Data"
	
	#process Jumplist files with jl.pl
	if(offset != "FOLDER"):
		jl_command = "perl /usr/local/src/windows-perl/jl.pl -u " + "'" + profile + "'" + " -f " + "'" + full_path + "'" + " >> " + "'" + folder_path + "/Processed_Files_" + str(offset) + "/JUMPLIST_DATA/jumplist_metadata.txt" + "'"
		jl_command_tln = "perl /usr/local/src/windows-perl/jl.pl -u " + "'" + profile + "'" + " -t -f " + "'" + full_path + "'" + " >> " + "'" + folder_path +  "/Processed_Files_" + str(offset) + "/JUMPLIST_DATA/jumplist_metadata_tln.txt" + "'"
		parse_command = "perl /usr/local/src/windows-perl/parse.pl -f " + "'" + folder_path + "/Processed_Files_" + str(offset) + "/JUMPLIST_DATA/jumplist_metadata_tln.txt" + "'" + "> " + "'" + folder_path + "/Processed_Files_" + str(offset) + "/JUMPLIST_DATA/jumplist_timeline.txt" + "'"
		outfile.write("The jl_command_tln is: " + jl_command_tln)
	else:
		jl_command = "perl /usr/local/src/windows-perl/jl.pl -u " + "'" + profile + "'" + " -f " + "'" + full_path + "'" + " >> " + "'" + folder_path + "/Processed_Files_FOLDER/JUMPLIST_DATA/jumplist_metadata.txt" + "'"
		jl_command_tln = "perl /usr/local/src/windows-perl/jl.pl -u " + "'" + profile + "'" + " -t -f " + "'" + full_path + "'" + " >> " + "'" + folder_path +  "/Processed_Files_FOLDER/JUMPLIST_DATA/jumplist_metadata_tln.txt" + "'"
		parse_command = "perl /usr/local/src/windows-perl/parse.pl -f " + "'" + folder_path + "/Processed_Files_FOLDER/JUMPLIST_DATA/jumplist_metadata_tln.txt" + "'" + "> " + "'" + folder_path + "/Processed_Files_FOLDER/JUMPLIST_DATA/jumplist_timeline.txt" + "'"
		outfile.write("The jl_command_tln is: " + jl_command_tln)
		
	subprocess.call([jl_command_tln], shell=True)
	subprocess.call([jl_command], shell=True)

	#create timeline
	outfile.write("The parse_command is: " + parse_command + "\n")
	subprocess.call([parse_command], shell=True)


