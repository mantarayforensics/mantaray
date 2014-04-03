#!/usr/bin/env python3
#This program will mount a DD or E01 Image and then recurse through each partition looking for 
#files that contain EXIF data.  When these files are found the exif data is extracted using
#exiftool(Phil Harvey).
#INPUT: NONE
#OUTPUT: creates a text file containing the metadata for every file found

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
from get_case_number import *
from get_output_location import *
from select_file_to_process import *
from parted import *
from mount import *
from mount_ewf import *
from done import *
from unix2dos import *
from mmls import *
from check_for_folder import *
from mount_encase_v6_l01 import *

import os
from os.path import join
import re
import io
import sys
import string
import subprocess
import datetime

### PROCESS ################################################################################################

def process_folder(mount_point, valid_extensions, item_to_process, outfile, folder_path):

	for root,dirs,files in os.walk(mount_point):
		for filenames in files:
			fileName, fileExtension = os.path.splitext(filenames)
					
			#replace the . in the file extension with nothing
			file_extension = fileExtension.replace('.','')	
			file_extension = file_extension.upper()				
			file_name = os.path.basename(fileName)
			for extension in valid_extensions:
				if(file_extension == extension):
					print("Running exiftool against file: " + filenames)
					outfile.write("Running exiftool against file: " + filenames)

					#chdir to output foler
					os.chdir(folder_path)
						
					#get absolute path to file
					file_name = os.path.join(root,filenames)
					quoted_file_name = "'" +file_name +"'"

					#enclose strings in quotes
					quoted_root = "'" +root +"'"	
								

					#set up exiftool command			
					exif_command = "exiftool -ext " + extension + " -l -sep *********** -z " + quoted_file_name + " >> " + "'" +  folder_path + "/Exif_data_" + item_to_process + ".txt" + "'"
										
					#print("The exif command is: " + exif_command + "\n\n")
					outfile.write("The exif command is: " + exif_command + "\n\n")

					#execute the exif command
					subprocess.call([exif_command], shell=True)
					#exif_out.write("\n\n")
	

############################################################################################################

def exifdata_mr(item_to_process, case_number, root_folder_path, evidence):
	print("The item to process is: " + item_to_process)
	print("The case_name is: " + case_number)
	print("The output folder is: " + root_folder_path)
	print("The evidence to process is: " + evidence)

	evidence_no_quotes = evidence

	evidence = '"' + evidence + '"'

	#get datetime
	now = datetime.datetime.now()

	#set Mount Point
	mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")
	
	#create output folder path
	folder_path = root_folder_path + "/" + "EXIF_Tool"
	check_for_folder(folder_path, "NONE")
	

	#open a log file for output
	log_file = folder_path + "/EXIF_Tool_logfile.txt"
	outfile = open(log_file, 'wt+')

	#set up tuple holding all of the file extensions exiftool can process
	valid_extensions = ('3FR', '3G2', '3GP2', '3GP', '3GPP', 'ACR', 'AFM', 'ACFM', 'AMFM', 'AI', 'AIT', 'AIFF', 'AIF', 'AIFC', 'APE', 'ARW', 'ASF', 'AVI', 'BMP', 'DIB', 'BTF', 'TIFF', 'TIF', 'CHM', 'COS', 'CR2', 'CRW', 'CIFF', 'CS1', 'DCM', 'DC3', 'DIC', 'DICM', 'DCP', 'DCR', 'DFONT', 'DIVX', 'DJVU', 'DJV', 'DNG', 'DOC', 'DOT', 'DOCX', 'DOCM', 'DOTX', 'DOTM', 'DYLIB', 'DV', 'DVB', 'EIP', 'EPS', 'EPSF', 'EXR', 'PS', 'ERF', 'EXE', 'DLL', 'EXIF', 'F4A', 'F4B', 'F4P', 'F4V', 'FFF', 'FLA', 'FLAC', 'FLV', 'FPX', 'GIF', 'GZ', 'GZIP', 'HDP', 'HDR', 'WDP', 'HTML', 'HTM', 'XHTML', 'ICC', 'ICM', 'IIQ', 'IND', 'INDD', 'INDT', 'INX', 'ITC', 'JP2', 'JPF', 'JPM', 'JPX', 'JPEG', 'JPC', 'JPG', 'J2C', 'J2K', 'K25', 'KDC', 'KEY', 'KTH', 'LNK', 'M2TS', 'MTS', 'M2T', 'TS', 'M4A', 'M4B', 'M4P', 'M4V', 'MEF', 'MIE', 'MIFF', 'MIF', 'MKA', 'MKV', 'MKS', 'MOS', 'MOV', 'Q', 'MP3', 'MP4', 'MPC', 'MPEG', 'MPG', 'M2V', 'MPO', 'MQV', 'QT', 'MRW', 'MXF', 'NEF', 'NMBTEMPLATE', 'NRW', 'NUMBERS', 'ODB', 'ODC', 'ODF', 'ODG', 'OGI', 'ODP', 'ODS', 'ODT', 'OGG', 'ORF', 'OTF', 'PAGES', 'PDF', 'PEF', 'PFA', 'PFB', 'PFM', 'PGF', 'PICT', 'PCT', 'PMP', 'PNG', 'JNG', 'MNG', 'PPM', 'PBM', 'PGM', 'PPT', 'PPS', 'POT', 'POTX', 'POTM', 'PPSX', 'PPSM', 'PPTX', 'PPTM', 'PSD', 'PSB', 'PSP', 'PSPIMAGE', 'QTIF', 'QTI', 'QIF', 'RAF', 'RAM', 'RPM', 'RAW', 'RAR', 'RAW', 'RIFF', 'RIF', 'RM', 'RV', 'RMVB', 'RSRC', 'RTF', 'RW2', 'RWL', 'RWZ', 'SO', 'SR2', 'SRF', 'SRW', 'SVG', 'SWF', 'THM', 'THMX', 'TIFF', 'TIF', 'TTF', 'TTC', 'VOB', 'VRD', 'VSD', 'WAV', 'WEBM', 'WEBP', ',WMA', 'WMV', 'X3F', 'XCF', 'XLS', 'XLT', 'XLSX', 'XLSM', 'XLSB', 'XLTX', 'XLTM', 'XMP', 'ZIP')

	if(item_to_process =="EnCase Logical Evidence File"):

		file_to_process = evidence
		mount_point = mount_encase_v6_l01(case_number, file_to_process, outfile)
		process_folder(mount_point, valid_extensions, item_to_process)

		#umount
		if(os.path.exists(mount_point)):
			subprocess.call(['sudo umount -f ' + mount_point], shell=True)
			os.rmdir(mount_point)


	if(item_to_process == "Directory"):

		mount_point = evidence_no_quotes
		process_folder(mount_point, valid_extensions, item_to_process, outfile, folder_path)

	

	elif(item_to_process == "Bit-Stream Image"):

		#get datetime
		now = datetime.datetime.now()

		#set Mount Point
		mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")

		#select dd image to process	
		Image_Path = evidence

		#check if Image file is in Encase format
		if re.search(".E01", Image_Path):

			#strip out single quotes from the quoted path
			#no_quotes_path = Image_Path.replace("'","")
			#print("THe no quotes path is: " +  no_quotes_path)
			#call mount_ewf function
			Image_Path = mount_ewf(Image_Path, outfile, mount_point)

		#call mmls function
		partition_info_dict, temp_time = mmls(outfile, Image_Path)

		#get filesize of mmls_output.txt
		file_size = os.path.getsize("/tmp/mmls_output_" + temp_time + ".txt") 

		#if filesize of mmls output is 0 then run parted
		if(file_size == 0):
			print("mmls output was empty, running parted")
			outfile.write("mmls output was empty, running parted")
			#call parted function
			partition_info_dict, temp_time = parted(outfile, Image_Path)	

		else:

			#read through the mmls output and look for GUID Partition Tables (used on MACS)
			mmls_output_file = open("/tmp/mmls_output_" + temp_time + ".txt", 'r')
			for line in mmls_output_file:
				if re.search("GUID Partition Table", line):
					print("We found a GUID partition table, need to use parted")
					outfile.write("We found a GUID partition table, need to use parted\n")
					#call parted function
					partition_info_dict, temp_time = parted(outfile, Image_Path)

	
		#loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
		for key,value in partition_info_dict.items():

			#set up file object for output file
			output_file = folder_path + "/Exif_data_partition_offset_" + str(key) +".txt"
			print("The output_file is: " + output_file)
			exif_out = open(output_file, 'wt+')

			#disable auto-mount in nautilis - this stops a nautilis window from popping up everytime the mount command is executed
			cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false"
			try:
				subprocess.call([cmd_false], shell=True)
			except:
				print("Autmount false failed")

			#call mount sub-routine
			success_code, loopback_device_mount = mount(value,key,Image_Path, outfile, mount_point)

			if(success_code):
				print("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
				outfile.write("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
			else:
		
				print("We just mounted filesystem: " + value + " at offset:" + str(key) + ". Scanning for files of interest.....\n")
				outfile.write("We just mounted filesystem: " + value + " at offset:" + str(key) + "\n")
			

				#get the filename without extension
				for root,dirs,files in os.walk(mount_point):
					for filenames in files:
						fileName, fileExtension = os.path.splitext(filenames)
					
						#replace the . in the file extension with nothing
						file_extension = fileExtension.replace('.','')	
						file_extension = file_extension.upper()				
						file_name = os.path.basename(fileName)
						for extension in valid_extensions:
							if(file_extension == extension):
								print("Running exiftool against file: " + filenames)
								outfile.write("Running exiftool against file: " + filenames)

								#chdir to output foler
								os.chdir(folder_path)
						
								#get absolute path to file
								file_name = os.path.join(root,filenames)
								quoted_file_name = "'" +file_name +"'"

								#enclose strings in quotes
								quoted_root = "'" +root +"'"	
								
	
								#set up exiftool command			
								exif_command = "exiftool -ext " + extension + " -l -sep *********** -z " + quoted_file_name + " >> " + "'" +  folder_path + "/Exif_data_partition_offset_" + str(key) +".txt" + "'"
										
								#print("The exif command is: " + exif_command + "\n\n")
								outfile.write("The exif command is: " + exif_command + "\n\n")

								#execute the exif command
								subprocess.call([exif_command], shell=True)
								#exif_out.write("\n\n")
						

				#unmount and remove mount points
				if(os.path.exists(mount_point)): 
					subprocess.call(['sudo umount -f ' + mount_point], shell=True)
					os.rmdir(mount_point)
				#unmount loopback device if this image was HFS+ - need to run losetup -d <loop_device> before unmounting
				if not (loopback_device_mount == "NONE"):
					losetup_d_command = "losetup -d " + loopback_device_mount
					subprocess.call([losetup_d_command], shell=True)

			#close outfile
			exif_out.close()

	#program cleanup
	outfile.close()
	
	#remove mount points created for this program
	if(os.path.exists(mount_point)):
		if not (item_to_process == "Directory"):
			os.rmdir(mount_point)
	if(os.path.exists(mount_point+"_ewf")):
		subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
		os.rmdir(mount_point+"_ewf")

	#delete empty directories in output folder
	for root, dirs, files in os.walk(folder_path, topdown=False):	
		for directories in dirs:
			files = []
			dir_path = os.path.join(root,directories)
			files = os.listdir(dir_path)	
			if(len(files) == 0):
				os.rmdir(dir_path)

