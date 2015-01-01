#!/usr/bin/env python3
#This extracts data from xml plists
#

##########################COPYRIGHT INFORMATION############################
# Copyright (C) 2014 Douglas.Koster@mantech.com      					  #
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

import re


def get_system_version(plist_info, abs_file_path, md5, export_file, outfile, key_name):

    plist_type = type(plist_info)
    print("The plist type is: " +  str(plist_type))

    if(type(plist_info) is dict):
        export_file.write('File Path: ' + "\t" + abs_file_path + "\n")
        export_file.write('MD5: ' + "\t\t" + str(md5) + "\n\n")
        print(abs_file_path + " has a plist attribute that is a dict")

        process_dict(plist_info, outfile, export_file, key_name)

    elif(str(type(plist_info)) == "<class 'plistlib._InternalDict'>"):
        export_file.write('File Path: ' + "\t" + abs_file_path + "\n")
        export_file.write('MD5: ' + "\t\t" + str(md5) + "\n")
        print(abs_file_path + " has a plist attribute that is an internal dict")

        process_dict(plist_info, outfile, export_file, key_name)

def process_dict(dictionary_plist, outfile, export_file, key_name):
    #loop through dict plist
    for key,value in sorted(dictionary_plist.items()):
        if(key_name == key):
            print("The key is: " + key + " The key_name is: " + key_name)
            export_file.write(key + "=> " + value)

            #figure out cat type
            if(re.search('10.9', value)):
                export_file.write("(Mavericks)")
            elif(re.search('10.8', value)):
                export_file.write("(Mountain Lion)")
            elif(re.search('10.7', value)):
                export_file.write("(Lion)")
            elif(re.search('10.6', value)):
                export_file.write("(Snow Leopard)")
            elif(re.search('10.5', value)):
                export_file.write("(Leopard)")
            elif(re.search('10.4', value)):
                export_file.write("(Tiger)")
            elif(re.search('10.3', value)):
                export_file.write("(Panther)")
            elif(re.search('10.2', value)):
                export_file.write("(Jaguar)")
            elif(re.search('10.1', value)):
                export_file.write("(Puma)")
            elif(re.search('10.0', value)):
                export_file.write("(Kodiak)")

    return key
