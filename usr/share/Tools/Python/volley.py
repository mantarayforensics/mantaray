#import modules
from easygui import *
from check_for_folder import *

import os
from os.path import join
import re
import io
import sys
import string
import subprocess
from dateutil.parser import *

def volley_mr(case_number, root_folder_path,  evidence, profile_to_use):
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)
	
	#create output folder path
	folder_path = root_folder_path + "/" + "Volatility"
	check_for_folder(folder_path, "NONE")

	#create output folder path
	pid_path = root_folder_path + "/Volatility/PID"
	check_for_folder(pid_path, "NONE")
	
	#open a log file for output
	log_file = folder_path + "/Volatility_logfile.txt"
	outfile = open(log_file, 'at+')

	Image_Path = evidence

	#add quotes to image path in case of spaces
	quoted_path = "'"+Image_Path +"'"

	#allow user to use pre-selected profile name
	if profile_to_use == "NOPROFILESELECTED":

		#run first volatility command to get image type
		print("Checking RAM image for imageinfo information...This may take a few minutes....\n")
		imageinfo = subprocess.check_output(["vol -f " + quoted_path + " imageinfo"], shell=True, universal_newlines=True)
		print("The value of imageinfo is: " + imageinfo)
		outfile.write("The value of imageinfo is: " + imageinfo)

		#have user specify the image type
		profile_type = enterbox(msg="Please Enter the profile to use", title='Profile Type',default='',strip=True,image=None,root=None)

		print("Profile selected: " + profile_type)	

	else:
		print("Using profile " + profile_to_use)
		profile_type = profile_to_use

	piddict = {}
	piddicts = []
	pidind = []

	#run psscan
	print("\n\nDetecting PIDs in Memory Image...")
	vol_command = "vol --profile=" + profile_type + " -f " + quoted_path + " psscan" + " | awk '{print $2" + '","$3","$4","$1","$5","$6","$7","$8}' + "'" 
	pids_output = subprocess.check_output([vol_command], shell=True, universal_newlines=True)
	pid_list = pids_output.split("\n")
	for i,pid in enumerate(pid_list):
		pids = pid.split(",")
		if i == 1 or i == 0: 
			print ("")
		else:
			if len(pids) == 1:
				print("")
			else:
				pidind.append(pids[1])
				piddict["Name"] = pids[0]
				piddict["PID"] = pids[1]
				piddict["PPID"] = pids[2]
				piddict["Offset(P)"] = pids[3]
				piddict["PDB"] = pids[4]
				piddict["Time"] = parse(pids[5] + " " + pids[6])
				piddict["Timezone"] = pids[7]
				
				piddicts.append(piddict)
				piddict = {}


	for i,pid in enumerate(piddicts):
		pid_dir = pid['Name'] + "_" + pid['PID']

		#create output folder path
		pid_folder_path = root_folder_path + "/Volatility/PID/" + pid_dir
		check_for_folder(pid_folder_path, "NONE")

		plugins = ['memmap', 'dlllist', 'handles', 'vadinfo', 'malfind', 'impscan', 'apihooks', 'devicetree', 'driverscan', 'enumfunc', 'getservicesids', 'getsids', 'idt', 'imageinfo', 'kpcrscan', 'machoinfo', 'mbrparser', 'printkey', 'privs', 'psdispscan', 'ssdt', 'thrdscan', 'usnparser', 'vadtree', 'vmwareinfo']
		for n,plugin in enumerate(plugins):

			#run plugin
			print("\n\n" + pid_dir + " Running " + plugin + ".")
			vol_command = "vol --profile=" + profile_type + " -f " + quoted_path + " " + plugin + " -p " + pid['PID'] + " > " + "'" + pid_folder_path + "/" + plugin + ".txt"+"'"
			subprocess.call([vol_command], shell=True)
			print ("Completed plugin ", n + 1, "/", len(plugins), " on process ", i + 1, "/", len(piddicts))



	#close outfile
	outfile.close()

	#change dir into output folder
	os.chdir(folder_path)

	#run unix2dos on text files
	unix2dos_command = "sudo unix2dos *.txt"
	subprocess.call([unix2dos_command], shell=True)

