#!/usr/bin/env python3
#This extracts data from xml plists
#
#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2013 douglas.koster@mantech.com				 #
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

import re


def plist_parser_module(plist_info, abs_file_path, md5, export_file, outfile):

	plist_type = type(plist_info)
	print("The plist type is: " +  str(plist_type))

	if(type(plist_info) is dict):
		print(abs_file_path + " has a plist attribute that is a dict")
		process_dict(plist_info, outfile, export_file, abs_file_path, md5)

	elif(str(type(plist_info)) == "<class 'plistlib._InternalDict'>"):
		print(abs_file_path + " has a plist attribute that is an internal dict")
		process_dict(plist_info, outfile, export_file, abs_file_path, md5)
	elif(type(plist_info) is list):
		print(abs_file_path + " has a plist attribute that is a list")
		process_list(plist_info, outfile, export_file, abs_file_path, md5)

def process_string(string, abs_file_path, md5, export_file, outfile):

	#clean up binary information from string
	string = string.strip()
	string = re.sub("^Data\(b'",'', string)
	string = re.sub("'\)",'', string)
	print("The string is: " + string)
	export_file.write(string)		

def process_list(plist_info, outfile, export_file, abs_file_path, md5):
	print("Just got passed the following list: " + str(plist_info))

	for element in plist_info:
		print("The element in list is of type: " + str(type(element)))
		element_type=str(type(element))
		if(type(element) is dict):
			print("The element inside list is a dict\n")
			process_dict(dict(element), outfile, export_file, abs_file_path, md5)
		elif(element_type == "<class 'plistlib._InternalDict'>"):
			print("The element inside list is an internal dict\n")
			process_dict(dict(element), outfile, export_file, abs_file_path, md5)
		elif(type(element) is str):
			print(str(element) + " is a string")
			process_string(str(element), abs_file_path, md5, export_file, outfile)
		elif(type(element) is list):
			print("The element is a list")
			process_list(element, outfile, export_file, abs_file_path, md5)


def process_dict(dictionary_plist, outfile, export_file, abs_file_path, md5):
	print("Inside Process_dict")
	
	#loop through dict plist
	for key,value in sorted(dictionary_plist.items()):
		print("The value is: " + str(value))
		key = key.strip()
		print("The key is: " + key)
		print("The value is of type: " + str(type(value)))
		export_file.write("\n\n" + key + " => \t" )
		#the key is a value we want, now check the value type so we can gets its contents
		if(type(value) is list):
			#print("The value: " + str(value) + "is a list")
			for element in value:
				print("The element is: " + str(element))
				element_type=str(type(element))
				print("The type is: " + element_type)
				if(type(element) is dict):
					print("The element inside list is a dict\n")
					process_dict(dict(element), outfile, export_file, abs_file_path, md5)
				elif(element_type == "<class 'plistlib._InternalDict'>"):
					print("The element inside list is an internal dict\n")
					process_dict(dict(element), outfile, export_file, abs_file_path, md5)
				elif(type(element) is str):
					print(str(element) + " is a string")
					process_string(str(element), abs_file_path, md5, export_file, outfile)
				elif(type(element) is list):
					print("The element is a list")
					process_list(element, outfile, export_file, abs_file_path, md5)
				elif(str(type(element)) == "<class 'datetime.datetime'>"):
					print(str(element))
					process_string(str(element), abs_file_path, md5, export_file, outfile)
				elif(str(type(element)) == "<class 'bool'>"):
					print(str(element))
					process_string(str(element), abs_file_path, md5, export_file, outfile)
				elif(str(type(element)) == "<class 'plistlib.Data'>"):
					print(str(element))
					process_string(str(element), abs_file_path, md5, export_file, outfile)
				elif(str(type(element)) == "<class 'int'>"):
					print(str(element))
					process_string(str(element), abs_file_path, md5, export_file, outfile)
		elif(type(value) is dict):
			print("The value inside list is a dict\n")
			process_dict(dict(value), outfile, export_file, abs_file_path, md5)
		elif(str(type(value)) == "<class 'plistlib._InternalDict'>"):
			print("The value inside list is an internal dict\n")
			process_dict(dict(value), outfile, export_file, abs_file_path, md5)			
		elif(type(value) is str):
			print(str(value) + " is a string")
			process_string(str(value), abs_file_path, md5, export_file, outfile)
		elif(type(value) is list):
			print("The value is a list")
			process_list(value, outfile, export_file, abs_file_path, md5)
		elif(str(type(value)) == "<class 'datetime.datetime'>"):
			print(str(value))
			process_string(str(value), abs_file_path, md5, export_file, outfile)
		elif(str(type(value)) == "<class 'bool'>"):
			print(str(value))
			process_string(str(value), abs_file_path, md5, export_file, outfile)
		elif(str(type(value)) == "<class 'plistlib.Data'>"):
			print(str(value))
			process_string(str(value), abs_file_path, md5, export_file, outfile)
		elif(str(type(value)) == "<class 'int'>"):
			print(str(value))
			process_string(str(value), abs_file_path, md5, export_file, outfile)
			
		
