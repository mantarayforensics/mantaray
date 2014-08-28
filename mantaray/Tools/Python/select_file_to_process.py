### GET IMAGE TO PROCESS #############################################################################################
#DESCRIPTION: This module uses easygui to ask the user to select an image file to process
#INPUT: Path to logfile or "NONE" if logging is not required
#OUTPUT: Returns the absolute path to the image file surrounded by single quotes to deal with spaces

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

from share.Tools.Python.easygui import *
import sys

def select_file_to_process(outfile):
	#this function asks the user to select a disk image to process via a GUI
	#if the path to a logfile is passed then write out data to logfile

	Image_Path = fileopenbox(msg="Select File to Process",title="Select File",default='/mnt/hgfs/*.*')
	#Image_Path = fileopenbox(msg="Select File to Process",title="Select File",default=None)
	if Image_Path == None:
		print ("Image File not specified")
		sys.exit(0)
	else:
		print("*************************************************************************")	
		print("File selected: " + Image_Path)
		print("*************************************************************************", end = "\n\n")

		if(outfile != "NONE"):
			outfile.write("File selected: " + Image_Path + "\n\n")

	#add quotes to image path in case of spaces
	quoted_path = "'" +Image_Path +"'"

	
	
	#return the quoted path
	return quoted_path

### GET IMAGE TO PROCESS #############################################################################################
