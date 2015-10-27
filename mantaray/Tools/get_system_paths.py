### FIND SYSTEM PATHS #####################################################################
#DESCRIPTION: This module looks for Windows Registry Hives recursively in a folder structure
#INPUT: filesystem, Bool whether to print or not, location of logfile, mount_point
#OUTPUT: LIST containing either "NONE" or absolute path to Registry hive (ex: /mnt/windows_mount/WINDOWS/SYSTEM32/config/SYSTEM)

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2011 		dougkoster@hotmail.com	                     #
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

#initialize variables
system_hive_path = "NONE"
system_hive_regback_path = "NONE"
sam_hive_path = "NONE"
sam_hive_regback_path = "NONE"
software_hive_path = "NONE"
software_hive_regback_path = "NONE"
security_hive_path = "NONE"
security_hive_regback_path = "NONE"
paths = []
paths = ["NONE", "NONE", "NONE", "NONE","NONE", "NONE","NONE", "NONE"]

def get_system_paths(value, prnt, outfile, mount_point):

	#initialize variables
	system_hive_path = "NONE"
	system_hive_regback_path = "NONE"
	sam_hive_path = "NONE"
	sam_hive_regback_path = "NONE"
	software_hive_path = "NONE"
	software_hive_regback_path = "NONE"
	security_hive_path = "NONE"
	security_hive_regback_path = "NONE"
	paths = []
	paths = ["NONE", "NONE", "NONE", "NONE","NONE", "NONE","NONE", "NONE"]


	#process Windows systems
	if (value == "hfs+"):
		print ("Don't need to look for registry hives since this partition is hfs+")
		if(outfile != "NONE"):
			outfile.write("Don't need to look for registry hives since this partition is hfs+\n")
	elif (value == "ext"):
		print ("Don't need to look for registry hives since this partition is ext")
		if(outfile != "NONE"):
			outfile.write("Don't need to look for registry hives since this partition is ext2\n")
	elif (value == "ext3"):
		print ("Don't need to look for registry hives since this partition is ext3")
		if(outfile != "NONE"):
			outfile.write("Don't need to look for registry hives since this partition is ext3\n")
	elif (value == "ext4"):
		print ("Don't need to look for registry hives since this partition is ext4")
		if(outfile != "NONE"):
			outfile.write("Don't need to look for registry hives since this partition is ext4\n")
	else: 
		if(value == "fat32"):
			print ("Look for registry hives since this partition is Windows and formatted fat32")
		if(outfile != "NONE"):
			outfile.write("Look for registry hives since this partition is Windows and formatted fat32\n")
		if(value == "ntfs"):
			print ("Look for registry hives since this partition is Windows and formatted ntfs")
		if(outfile != "NONE"):
			outfile.write("Look for registry hives since this partition is Windows and formatted ntfs\n")
		
		#set up print border
		if(prnt == "YES"):
			print("***********REGISTRY FILE LOCATIONS***********************************")
		if(outfile != "NONE"):
			outfile.write("***********REGISTRY FILE LOCATIONS***********************************\n")


		#get path to system hive
		for root,dirs,files in os.walk(mount_point):
			for filenames in files:
				if (os.path.join(root,filenames).lower() == mount_point + '/windows/system32/config/system'):
					system_hive_path = os.path.join(root,filenames)
					paths[0] = system_hive_path
					if(prnt == "YES"):					
						print("SYSTEM HIVE: " + system_hive_path)
					if (outfile != "NONE"):
						outfile.write("SYSTEM HIVE: " + system_hive_path + "\n")
				elif (os.path.join(root,filenames).lower() == mount_point + '/windows/system32/config/regback/system'):
					system_hive_regback_path = os.path.join(root,filenames)
					paths[1] = system_hive_regback_path
					if(prnt == "YES"):					
						print("SYSTEM HIVE REGBACK: " + system_hive_regback_path)
					if (outfile != "NONE"):
						outfile.write("SYSTEM HIVE REGBACK: " + system_hive_regback_path + "\n")
		#get path to sam hive
		for root,dirs,files in os.walk(mount_point):
			for filenames in files:
				if (os.path.join(root,filenames).lower() == mount_point + '/windows/system32/config/sam'):
					sam_hive_path = os.path.join(root,filenames)
					paths[2] = sam_hive_path
					if(prnt == "YES"):				
						print("SAM HIVE: " + sam_hive_path)
					if(outfile != "NONE"):
						outfile.write("SAM HIVE: " + sam_hive_path + "\n")
				elif (os.path.join(root,filenames).lower() == mount_point + '/windows/system32/config/regback/sam'):
					sam_hive_regback_path = os.path.join(root,filenames)
					paths[3] = sam_hive_regback_path
					if(prnt == "YES"):
						print("SAM HIVE REGBACK: " + sam_hive_regback_path)
					if(outfile != "NONE"):
						outfile.write("SAM HIVE REGBACK: " + sam_hive_regback_path + "\n")
		#get path to software hive
		for root,dirs,files in os.walk(mount_point):
			for filenames in files:
				if (os.path.join(root,filenames).lower() == mount_point + '/windows/system32/config/software'):
					software_hive_path = os.path.join(root,filenames)
					paths[4] = software_hive_path
					if(prnt == "YES"):
						print("SOFTWARE HIVE: " + software_hive_path)
					if(outfile != "NONE"):
						outfile.write("SOFTWARE HIVE: " + software_hive_path + "\n")
				elif (os.path.join(root,filenames).lower() == mount_point + '/windows/system32/config/regback/software'):
					software_hive_regback_path = os.path.join(root,filenames)
					paths[5] = software_hive_regback_path
					if(prnt == "YES"):
						print("SOFTWARE HIVE REGBACK: " + software_hive_regback_path)
					if(outfile != "NONE"):
						outfile.write("SOFTWARE HIVE REGBACK: " + software_hive_regback_path + "\n")

		#get path to security hive
		for root,dirs,files in os.walk(mount_point):
			for filenames in files:
				if (os.path.join(root,filenames).lower() == mount_point + '/windows/system32/config/security'):
					security_hive_path = os.path.join(root,filenames)
					paths[6] = security_hive_path
					if(prnt == "YES"):
						print("SECURITY HIVE: " + security_hive_path)
					if(outfile != "NONE"):
						outfile.write("SECURITY HIVE: " + security_hive_path + "\n")
				elif (os.path.join(root,filenames).lower() == mount_point + '/windows/system32/config/regback/security'):
					security_hive_regback_path = os.path.join(root,filenames)
					paths[7] = security_hive_regback_path
					if(prnt == "YES"):
						print("SECURITY HIVE REGBACK: " + security_hive_regback_path)
					if(outfile != "NONE"):
						outfile.write("SECURITY HIVE REGBACK: " + security_hive_regback_path + "\n")

		#close print border
		if(prnt == "YES"):		
			print("***********REGISTRY FILE LOCATIONS***********************************\n\n")
		if(outfile != "NONE"):
			outfile.write("***********REGISTRY FILE LOCATIONS************************************\n\n")

		return paths

		

### FIND SYSTEM PATHS ####
