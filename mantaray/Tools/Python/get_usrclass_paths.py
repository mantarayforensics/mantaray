### GET USRCLASS.DAT FILES ################################################################
#DESCRIPTION: This module finds the absolute path to each USRCLASS.DAT file within a given mount point
#INPUT: absolute path to mount point (ex: "/mnt/windows_mount")
#OUTPUT: returns a list containing the absolute path to each USRCLASS.DAT file found in that partition

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

def get_usrclass_paths(mount_point):
	#initialize tuple
	usrclass_dat = []
	#root_string_length = 0
	#rightmost_slash_location = 0

	#get paths to all USRCLASS.DAT files
	for root,dirs,files in os.walk(mount_point):
		for filenames in files:
			if(filenames.endswith('USRCLASS.DAT')) or (filenames.endswith('usrclass.dat')) or (filenames.endswith('UsrClass.dat')):		
				#append the full path to each USRCLASS.dat file to list usrclass_dat
				usrclass_dat.append(os.path.join(root,filenames))
				
				
	print("The  USRCLASS.DAT files are: *********************************************")	
	for items in usrclass_dat:
		print (items)
	print("*********************************************************************",end = "\n\n")	
	return (usrclass_dat)

### GET USRCLASS FILES ####
