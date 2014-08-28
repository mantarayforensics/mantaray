### GET OUTPUT LOCATION ##############################################################################
#DESCRIPTION: This module uses easygui to ask the user to select an output location for results to be stored
#INPUT: case_number (string)
#OUTPUT: folder_path (output location chosen which is a folder plus the case name)

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

import os
import datetime

from share.Tools.Python.easygui import *
import sys


def get_output_location(case_number):
	output_location = diropenbox(msg="Output Location",title="Choose Path",default='/mnt/hgfs/')
	if output_location == None:
		print("Output path not specified")
		sys.exit(0)
	else:
		output_location = output_location + "/"

	#join the case number and output location into a single path variable	
	folder_path = os.path.join(output_location,case_number)

	#check to see if the folder exists, if not create it
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
		print("Just created output folder: " + folder_path)
	else:
		print("Output folder: " + folder_path + " already exists - appending date/time.")
		#get datetime
		now = datetime.datetime.now()
		os.makedirs(folder_path + "_" + now.strftime("%Y-%m-%d_%H_%M_%S"))
		print("Just created output folder: " + folder_path + "_" + now.strftime("%Y-%m-%d_%H_%M_%S"))
		folder_path = folder_path + "_" + now.strftime("%Y-%m-%d_%H_%M_%S")

	return folder_path

### GET OUTPUT LOCATION ###
