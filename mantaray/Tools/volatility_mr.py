#!/usr/bin/env python3
#This program runs Volatility 2.4 modules against either a RAM image or (decompressed hiberfil.sys file - future version)
#
#ManTech International Corporation
#
##########################COPYRIGHT INFORMATION############################
# Copyright (C) 2015 Kevin.Murphy@mantech.com, ManTech International      #
# MantaRay Team: mantarayforensics@mantech.com				  #
# This program is free software: you can redistribute it and/or modify    #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# This program is distributed in the hope that it will be useful,         #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program.  If not, see http://www.gnu.org/licenses/.     #
##########################COPYRIGHT INFORMATION############################
#
#Last Updated: October 2015
version = 'Volatility Module v2.00.00'
#
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
from subprocess import Popen, PIPE

#define supported plugins

#no support; no planned development; run plugin manually
suppress_list = ['volshell']

#not currently supported; development in progress
plugin_not_currently_supported = ['cachedump','dumpfiles','dlldump','dumpcerts','evtlogs','hibinfo',\
				'hivedump','imagecopy','impscan','memdump','moddump','patcher',\
				'poolpeek','procdump','raw2dmp','screenshot','ssdeepscan', 'strings',\
				'vaddump','yarascan']

def plugin_operating_system_support(plugin):
	"""
	This function passes the os type to the master GUI. and defines the os type for known/unknown plugins.
	"""

	#list of known plugins
	operating_system_support_list = ['apihooks:XP/VISTA/WIN7', 'apihooksdeep:XP/VISTA/WIN7', 'atoms:XP/VISTA/WIN7', 'atomscan:XP/VISTA/WIN7', \
	'auditpol:XP/VISTA/WIN7', 'autoruns:XP/VISTA/WIN7', 'bigpools:', 'bioskbd:', 'callbacks:', 'chromecookies:', \
	'chromedownloadchains:', 'chromedownloads:', 'chromehistory:', 'chromesearchterms:', \
	'chromevisits:', 'clipboard:', 'cmdline:', 'cmdscan:', 'connections:XP/Win2003', \
	'connscan:', 'consoles:', 'crashinfo:', 'deskscan:', 'devicetree:', 'dlllist:', 'driverbl:', \
	'driverirp:', 'driverscan:', 'editbox:', 'envars:', 'eventhooks:', 'filescan:', 'firefoxcookies:', \
	'firefoxdownloads:', 'firefoxhistory:', 'gahti:', 'gditimers:', 'gdt:', 'getservicesids:', 'getsids:', \
	'handles:', 'hashdump:','hivelist:', 'hivescan:', 'hpakextract:', 'hpakinfo:', 'idt:', 'idxparser:', 'iehistory:', \
	'imageinfo:', 'joblinks:', 'kdbgscan:', 'kpcrscan:', 'ldrmodules:', 'limeinfo:', 'lsadump:', 'machoinfo:', \
	'malfind:', 'malfinddeep:', 'malprocfind:', 'malsysproc:', 'mbrparser:', 'memmap:', 'messagehooks:', \
	'mftparser:', 'mimikatz:', 'modscan:', 'modules:', 'multiscan:', 'mutantscan:', 'netscan:Vista/Win7', 'notepad:', \
	'objtypescan:', 'pooltracker:Vista/Win7', 'prefetchparser:', 'printkey:', 'privs:', 'processbl:', 'pslist:', \
	'psscan:', 'pstotal:', 'pstree:', 'psxview:', 'servicebl:', 'sessions:', 'shellbags:', 'shimcache:', \
	'sockets:XP', 'sockscan:XP', 'ssdt:', 'strings:', 'svcscan:', 'symlinkscan:', 'thrdscan:', 'threads:', \
	'timeliner:', 'timers:', 'truecryptmaster:', 'truecryptpassphrase:', 'truecryptsummary:', \
	'trustrecords:', 'uninstallinfo:', 'unloadedmodules:', 'userassist:', 'userhandles:', \
	'usnparser:', 'vadinfo:', 'vadtree:', 'vadwalk:', 'vboxinfo:', 'verinfo:', 'vmwareinfo:', \
	'windows:', 'wintree:', 'wndscan:']

	OStype = 'NONE'	

	for item in operating_system_support_list:
		if re.search(plugin,item):
			#print("Item",item)
			item_split = item.split(':')
			#print("Item split",item_split)
			item_split2 = item_split[1]
			#print("Item split2","'",item_split2)
			if item_split2 == "":
				OStype = "Unknown Support"
				#print('OStypt:',OStype)
			else:
				OStype = item_split2
				#print('OStypt:',OStype)

	if OStype == 'NONE':		
		for item in plugin_not_currently_supported:
			if re.search(plugin,item):
				OStype = "In development; no GUI support"
				#print('OStypt:',OStype)

	if OStype == 'NONE':
		for item in suppress_list:
			if re.search(plugin,item):
				OStype = "Not Supported"
				#print('OStypt:',OStype)

	if OStype == 'NONE':
		OStype = "Unknown to GUI; New plugin?"
		#print('OStypt:',OStype)
					
	#print("OStype leaving the vol function:",OStype)
	return(OStype)


def error_logging(outfile,folder_path,selected_profile,plugin,output,win_plugins_error):
	"""
	This function is for error logging the Volatility_mr.py processing.
	"""
	
	stderr = str(output.communicate()[1])
	if re.search("\\n", stderr):
		#split stderr to grab error
		error_list = stderr.split('\\n')
		error = error_list[1]
	else:
		error = stderr
		###debug printing###
		#print("This is stderr:",stderr)

	error_warning_list = ['ERROR','WARNING']

	#count errors
	count = 0

	for err in error_warning_list:

		#search for errors
		if re.search(err, stderr):
			
			#open a log file for error output
			error_log_file = folder_path + "/Volatility_logfile_errors.txt"
			error_outfile = open(error_log_file, 'a')#'wt+')
			#log errors in standard log and error log
			print(plugin,"encountered an ERROR/WARNING; check options/configuration/logs")
			print("Processing did not finish successfully...")

			##debug printing###
			#print(error)
			#outfile.write("")
			outfile.write(plugin + " encountered an ERROR/WARNING\n")
			#outfile.write("")
			outfile.write(error + "\n\n")
			
			#error_outfile.write("")
			error_outfile.write(plugin + " encountered an ERROR/WARNING\n")
			#error_outfile.write("")
			error_outfile.write(error + "\n\n")
			
			#log Windows errors for reporting
			windows = ['Win','Vista']
			for item in windows:
				if re.search(item, selected_profile):
					win_plugins_error.append(plugin)
			count = 1
			error_outfile.close()

	#Report successful process
	if count == 0:
		print("Finished successfully...")
		outfile.write("")
		outfile.write("Plugin: " + plugin + "\n")
		outfile.write("Finished successfully...\n\n")

def volatility_mr(case_number, root_folder_path,  evidence, selected_profile, selected_plugin, selected_plugin_descr, complete_plugin_list):

	###Debug testing code###
	#print("The case_name is: " + case_number)
	#print("The output folder is: " + root_folder_path)
	#print("The evidence to process is: " + evidence)
	
	#create output folder path
	folder_path = root_folder_path + "/" + "Volatility"
	check_for_folder(folder_path, "NONE")
	
	#open a log file for output
	log_file = folder_path + "/Volatility_logfile.txt"
	outfile = open(log_file, 'wt+')

	Image_Path = evidence

	#add quotes to image path in case of spaces
	quoted_path = "'" + Image_Path + "'"

	#See Volatility Commands reference data (/usr/share/mantaray/docs/VolatilityUsage23.rst) for more information\n

	#start reporting lists####Still needs development; not being used at this time...
	win_plugins_complete = []
	win_plugins_not_supported = []
	win_plugins_skipped = []
	win_plugins_error = []

	###debug printing###
	#print("This is selected_plugin type:\n",type(selected_plugin))
	#print("This is selected_plugin:\n",selected_plugin)
	#print("This is selected_plugin_descr:\n",selected_plugin_descr)

	#print banner - MR
	print("\nMantaRay > " + version)
	print("mantarayforensics.com/forums/")
	print("matarayforeniscs@mantech.com")
	print("github.com/mantarayforensics/mantaray\n")

	#print banner - Vol
	print("Volatility v2.4")
	print("volatilityfoundation.org")
	print("volatility-labs.blogspot.com")
	print("github.com/volatilityfoundation/volatility\n")

	print("Processing requested plugins:")
	
	#run selected plugins
	for plugin in selected_plugin:

		if plugin in suppress_list:
			num_index = complete_plugin_list.index(plugin)
			#print("This is num_index:",num_index)
			descr = selected_plugin_descr[num_index]
			print("\nRunning " + plugin + "...")
			print(descr + "...")
			print("The plugin " + plugin + " is not supported...")
			print("This plugin has advanced features.  Run manually...")
			outfile.write("The plugin " + plugin + " is not supported...\n")
			outfile.write("This plugin has advanced features.  Run manually...\n\n")
			win_plugins_not_supported.append(plugin)
			continue

		if plugin in plugin_not_currently_supported:
			num_index = complete_plugin_list.index(plugin)
			#print("This is num_index:",num_index)
			descr = selected_plugin_descr[num_index]
			print("\nRunning " + plugin + "...")
			print(descr + "...")
			print("The plugin " + plugin + " is not currently supported...")
			print("Support may be added in a future release...")
			print("Check GitHub for updates...")
			print("github.com/mantarayforensics/mantaray")
			print("Currently running:",version)
			outfile.write("The plugin " + plugin + " is not currently supported.\n")
			outfile.write("Support may be added in a future release.\n")
			outfile.write("Check GitHub for updates...\n")
			outfile.write("github.com/mantarayforensics/mantaray\n")
			outfile.write("The plugin was skipped.\n\n")
			win_plugins_skipped.append(plugin)
			continue

		if plugin == 'pstotal':
			num_index = complete_plugin_list.index('pstotal')
			#print("This is num_index:",num_index)
			descr = selected_plugin_descr[num_index]
			plugin = 'pstotal.dot.full-graph'
			print("\nRunning pstotal...")

			
			pstotal_command = "vol.py --profile=" + selected_profile + " -f " + quoted_path \
			+ " pstotal --output=dot > " + "'" + folder_path + \
			"/pstotal.dot.full-graph.txt" + "'"
			print("Processing DOT output for full process graph...")
			output = Popen([pstotal_command], shell=True, stderr=PIPE)
			error_logging(outfile,folder_path,selected_profile,plugin,output,win_plugins_error)
			
			pstotal_hidden_command = "vol.py --profile=" + selected_profile + " -f " + quoted_path \
			+ " pstotal --output=dot -S -C > " + "'" + folder_path + \
			"/pstotal.dot.hidden-only-graph.txt" + "'"
			print("Processing DOT output for only hidden process graph...")
			output = Popen([pstotal_hidden_command], shell=True, stderr=PIPE)
			plugin = 'pstotal.dot.hidden-only-graph'
			error_logging(outfile,folder_path,selected_profile,plugin,output,win_plugins_error)

			pstotal_text_command = "vol.py --profile=" + selected_profile + " -f " + quoted_path + \
			" pstotal --output=text > " + "'" + folder_path + \
			"/pstotal.text-only.txt" + "'"
			print("Processing text output for hidden processes...")
			output = Popen([pstotal_text_command], shell=True, stderr=PIPE)
			plugin = 'pstotal.text-only'
			error_logging(outfile,folder_path,selected_profile,plugin,output,win_plugins_error)

			pstotal_graphviz_command1 = "dot -Tpng " + "'" + folder_path + "/pstotal.dot.full-graph.txt" \
			+ "'" + " -o " + "'" + folder_path + \
			"/pstotal.dot.full-graph.png" + "'"
			print("Running Graphviz to create full graph (PNG)...")
			output = Popen([pstotal_graphviz_command1], shell=True, stderr=PIPE)
			plugin = 'pstotal.dot.full-graph'
			error_logging(outfile,folder_path,selected_profile,plugin,output,win_plugins_error)

			pstotal_graphviz_command2 = "dot -Tpng " + "'" + folder_path + "/pstotal.dot.hidden-only-graph.txt" \
			+ "'" + " -o " + "'" + folder_path + \
			"/pstotal.dot.hidden-only-graph.png" + "'"
			print("Running Graphviz to create hidden graph (PNG)...")
			output = Popen([pstotal_graphviz_command2], shell=True, stderr=PIPE)
			plugin = 'pstotal.dot.hidden-only-graph'
			error_logging(outfile,folder_path,selected_profile,plugin,output,win_plugins_error)

			plugin = 'pstotal'
			win_plugins_complete.append(plugin)
			continue

		xp_2003_only_plugins = ['connections', 'evtlogs']

		if plugin in xp_2003_only_plugins: 
			if re.search('XP', selected_profile):
				print("\nRunning [Windows XP and 2003 Only] plugin...")

			elif re.search('2003', selected_profile):
				print("\nRunning [Windows XP and 2003 Only] plugin...")

			else:
				continue

		xp_only_plugins = ['sockets','sockscan']

		if plugin in xp_only_plugins: 
			if re.search('XP', selected_profile):
				print("\nRunning [Windows XP Only] plugin...")
			else:
				continue

		vista_and_newer_only_plugins = ['netscan','pooltracker']

		if plugin in vista_and_newer_only_plugins:
			os_support = ['Vista','Win7','Win8']  
			for os_type in os_support:
				if re.search(os_type, selected_profile):
					print("\nRunning Vista and newer only plugin...")
			else:
				continue

		####ADD NEW MODULE####
		#elif plugin == <plugin name>:	
		#	print("\nRunning " + plugin + "...")
		#	<plugin name>_command = "vol.py -f " + quoted_path + plugin + " > " \
		#	+ "'" + folder_path + "/<plugin name>.txt"+"'"
		#	output = Popen([<plugin name>_command], shell=True, stderr=PIPE)
		#	error_logging(outfile,folder_path,selected_profile,plugin,output,win_plugins_error)
		#	win_plugins_complete.append('devicetree')

		try:
			num_index = complete_plugin_list.index(plugin)
			#print("This is num_index:",num_index)
			descr = selected_plugin_descr[num_index]
			print("\nRunning " + plugin + "...")
			print(descr)					
			#print("This is plugin:\n",plugin)	
			processing_command = "vol.py --profile=" + selected_profile + " -f " + quoted_path + " " + plugin + " > " \
			+ "'" + folder_path + "/" + plugin + ".txt"+"'"
			#print("Vol Processing Command:",processing_command)
			output = Popen([processing_command], shell=True, stderr=PIPE)
			error_logging(outfile,folder_path,selected_profile,plugin,output,win_plugins_error)
			win_plugins_complete.append(plugin)

		except OSError as error:
			print("The plugin " + pluin + "experienced an OSError and failed, see log file...\n")
			outfile.write("The plugin " + plugin + " experienced an OSError and failed.\n")
			outfile.write(error + "\n")
		
	#close outfile
	outfile.close()

	#change permissions (option)
	#chmod_command = "chmod -R 777 " + root_folder_path
	#subprocess.call([chmod_command], shell=True)

	#change dir into output folder
	os.chdir(folder_path)

	#run text files through unix2dos
	for root, dirs, files in os.walk(folder_path):
		for filenames in files:
			#get file extension
			fileName, fileExtension = os.path.splitext(filenames)
			if(fileExtension.lower() == ".txt"):
				full_path = os.path.join(root,filenames)
				quoted_full_path = "'" +full_path+"'"
				print("Running Unix2dos against file: " + filenames)
				unix2dos_command = "sudo unix2dos " + quoted_full_path
				subprocess.call([unix2dos_command], shell=True)
