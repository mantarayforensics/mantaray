#!/usr/bin/env python3
#This program extracts triage data from selected plist files
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

import os
import re
import subprocess
import datetime
import shutil
import plistlib
import xml.parsers.expat as expat
import base64

from plist_parser_module import *
from get_system_version import *
from mount_encase_v6_l01 import *


def process_systemversion_plist(abs_file_path, export_file, md5, outfile):
    print("About to process: " + abs_file_path)
    abs_file_path_quotes = "'"+abs_file_path+"'"

    #process with plistlib
    plist_info = plistlib.readPlist(abs_file_path)

    #set keys to extract from sytemversion.plist
    key_name = "ProductVersion"

    #pass plist to plist_parser_module
    version = get_system_version(plist_info, abs_file_path, md5, export_file, outfile, key_name)

def process_system_plists(abs_file_path, export_file, md5, outfile, outfile_error):
    print("About to process: " + abs_file_path)
    abs_file_path_quotes = "'"+abs_file_path+"'"

    #process with plistlib
    plist_info = plistlib.readPlist(abs_file_path)

    #write out file metadata
    export_file.write("\n-------------------------------------------------------------------------------------------\n")
    export_file.write("\n" + 'File Path: ' + "\t" + abs_file_path + "\n")
    export_file.write('MD5: ' + "\t\t" + str(md5) + "\n\n")

    #pass plist to plist_parser_module
    plist_parser_module(plist_info, abs_file_path, md5, export_file, outfile)

def process_text_plists(abs_file_path, export_file, md5, outfile, key_name, outfile_error):
    print("About to process: " + abs_file_path)
    abs_file_path_quotes = "'"+abs_file_path+"'"

    #write out file metadata
    export_file.write("\n-------------------------------------------------------------------------------------------\n")
    export_file.write("\n" + 'File Path: ' + "\t" + abs_file_path + "\n")
    export_file.write('MD5: ' + "\t\t" + str(md5) + "\n\n")

    #open input file containing list of plists to process
    infile = open(abs_file_path, 'r+', encoding='utf-8')
    with open(infile) as f:
        line = f.readlines
        export_file.write(line + "\n")
def process_converted_binary_plist(temp_file_path, md5, export_file, outfile, abs_file_path):
    def start_element(name, attrs):
        print ('Start element:', name, attrs)
    def end_element(name):
            print ('End element:', name)
    def char_data(data):
        data_str = str(repr(data))
        data_str = data_str.strip()
        print(data_str)

        #clean up data
        data_str = data_str.replace("'","")
        data_str = data_str.replace("\\t\\t\\t\\t", "")
        data_str = data_str.replace("\\t\\t\\t", "")
        data_str = data_str.replace("\\t\\t", "")
        data_str = data_str.replace("\\t", "")
        data_str = data_str.replace("\\n", "")

        if (data_str != ""):
            if((len(data_str) % 4 == 0) and re.match('^[A-Za-z0-9+/]+[=]{0,2}$', data_str)):
                #non base64 strings can match above, but they all seem to have at least 2 caps in a row
                pattern = '[A-Z]{2}'
                if(re.search(pattern, data_str)):
                    print("This string is base64 since it contains 2 uppercase in a row")
                    try:
                        bytes = str.encode(data_str)
                        print("Successfully converted to bytes")
                        data = base64.b64decode(bytes)
                        print("Successfully decoded bytes into decode base64")
                        data2 = data.decode('unicode-escape')
                        print("Successfully decoded unicode characters")
                        #strip out non-ascii characters
                        data3 = ''.join([c for c in data2 if ord(c) > 31 or ord(c) == 9])
                        print(data2)
                        print (data3)
                        #data_string = data.decode(encoding='hex')
                        #print out only printable characters
                        export_file.write("\nBEGIN Decoded BASE64 data =>\n")
                        export_file.write(data3 + "\n" + "END Decoded BASE64 data\n\n")

                    except:
                        print(data_str + " is not base64")
                        export_file.write(data_str + "\n")
                else:
                    print(data_str + " is not base64 since it doesn't have 2 caps in a row")
                    export_file.write(data_str + "\n")
            else:
                export_file.write(data_str + "\n")

    #write out file metadata
    export_file.write("\n\n-------------------------------------------------------------------------------------------\n")
    export_file.write("\n" + 'File Path: ' + "\t" + abs_file_path + "\n")
    export_file.write('MD5: ' + "\t\t" + str(md5) + "\n\n")

    p = expat.ParserCreate()
    p.ordered_attributes=1
    p.buffer_text = 1

    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data

    p.ParseFile(open(temp_file_path, 'rb'))

def process_folder(folder_to_process, export_file, outfile, outfile_error, now):

    #initialize list of plist names to process
    #plists_to_process = ['com.apple.airport.preferences.plist', 'com.apple.sidebarlists.plist', 'com.apple.Bluetooth.plist' ]
    #plists_to_process = ['com.apple.airport.preferences.plist', 'com.apple.Bluetooth.plist' ]

    #open input file containing list of plists to process
    #infile = ('/usr/local/src/Manta_Ray/docs/plists_to_process.txt', encoding='utf-8')
    with open('/usr/local/src/Manta_Ray/docs/plists_to_process.txt') as f:
        plists_to_process = f.read().splitlines()

    print("Plists_to_process type is: " + str(type(plists_to_process)))
    print("The plists to process are: " + str(plists_to_process))
    #recurse once to find systemversion.plist to get OSX version
    for root,dirs,files in os.walk(folder_to_process):
        for file_name in files:
            fileName, fileExtension = os.path.splitext(file_name)
            abs_file_path = os.path.join(root,file_name)

            #check for plist extension and not link files
            if(fileExtension == ".plist") and not os.path.islink(abs_file_path):

                #get file size
                try:
                    file_size = os.path.getsize(abs_file_path)
                except:
                    print("Could not get filesize for file: " + abs_file_path)
                    outfile.write("Could not get filesize for file: " + abs_file_path + "\n")
                #process plist files that are not links and are not 0 in size
                if(file_size):
                    #Get OSX version First
                    if file_name == "SystemVersion.plist":
                        print("Plist to process is: " + file_name)

                        #get metadata
                        md5 = calculate_md5(abs_file_path)
                        print("The md5 is: " + md5)

                        #process SystemVersion.plist
                        process_systemversion_plist(abs_file_path, export_file, md5, outfile)
    for root,dirs,files in os.walk(folder_to_process):
        for file_name in files:
            fileName, fileExtension = os.path.splitext(file_name)
            abs_file_path = os.path.join(root,file_name)
            quoted_abs_file_path = '"'+abs_file_path+'"'

            #check if /tmp/binary_plists folder exists, if not create
            if not os.path.exists('/tmp/binary_plists/'):
                os.makedirs('/tmp/binary_plists/')
                #print("Just created folder: " + path)
                outfile.write("\nJust created output folder: /tmp/binary_plists/\n")
            else:
                #delete temp path
                shutil.rmtree('/tmp/binary_plists/')
                os.makedirs('/tmp/binary_plists/')

            #check for plist extension and not link files
            if(fileExtension == ".plist") and not os.path.islink(abs_file_path):

                #get file size
                try:
                    file_size = os.path.getsize(abs_file_path)
                except:
                    print("Could not get filesize for file: " + abs_file_path)
                    outfile.write("Could not get filesize for file: " + abs_file_path + "\n")
                #process plist files that are not links and are not 0 in size
                if(file_size):
                    #process other plists in the list
                    for plist in plists_to_process:
                        if file_name == plist:

                            #check if plist is binary
                            plist_file = open(abs_file_path, 'r', encoding='utf-8', errors='ignore')
                            first_line = plist_file.readline()
                            first_line = first_line.strip()

                            #get length of first line
                            length_first_line = len(first_line)

                            #grab lines from file until we get one that is longer than 3 characters
                            if(length_first_line > 3):
                                print("First line is over 3 characters long")
                            else:
                                first_line = plist_file.readline()

                            print("The first line is: " + first_line)

                            #close plist file
                            plist_file.close()

                            if(re.search('bplist', first_line)):
                                file_format = "binary_plist"
                                print(file_name + " is " + file_format)
                            elif(re.search('xml version', first_line)):
                                file_format = "xml_plist"
                                print(file_name + " is " + file_format)
                            else:
                                file_format = "text_plist"
                                print(file_name + " is " + file_format)

                            #get metadata
                            md5 = calculate_md5(abs_file_path)
                            md5 = md5.strip()
                            print("The md5 is: " + md5)

                            outfile.write("About to process: " + abs_file_path + "\n")
                            if(file_format == "xml_plist"):
                                process_system_plists(abs_file_path, export_file, md5, outfile, outfile_error)
                            elif(file_format == "binary_plist"):


                                #convert binary file
                                plutil_command = "plutil -i " + quoted_abs_file_path + " -o /tmp/binary_plists/" + file_name + "_" + md5 + ".plist"
                                print("The plutil command is: " + plutil_command)
                                try:
                                    subprocess.call([plutil_command], shell=True)
                                    outfile.write("The converted binary plist is named: /tmp/binary_plists/" + file_name + "_" + md5 + ".plist\n")
                                except:
                                    print("Call to plutil failed for file: " + abs_file_path)
                                    outfile_error.write("Call to plutil failed for file: " + abs_file_path + "\n")
                                process_converted_binary_plist("/tmp/binary_plists/" + file_name + "_" + md5 + ".plist", md5, export_file, outfile, abs_file_path)





def plist_processor(item_to_process, case_number, root_folder_path, evidence):
    print("The item to process is: " + item_to_process)
    print("The case_name is: " + case_number)
    print("The output folder is: " + root_folder_path)
    print("The evidence to process is: " + evidence)

    evidence_no_quotes = evidence
    evidence = '"' + evidence + '"'

    #get datetime
    now = datetime.datetime.now()

    #set Mount Point
    mount_point = "/mnt/" + "MantaRay_" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")

    #create output folder path
    folder_path = root_folder_path + "/" + "PLIST_Processor"
    check_for_folder(folder_path, "NONE")

    #open a log file for output
    log_file = folder_path + "/PLIST_processor_logfile.txt"
    outfile = open(log_file, 'wt+')

    #open an error file for output
    log_file = folder_path + "/PLIST_processor_error_log.txt"
    outfile_error = open(log_file, 'wt+')

    #open file to write output
    exp_file = folder_path + "/" + case_number +"_PLIST_Triage.txt"
    export_file = open(exp_file, 'a')

    if(item_to_process == "Directory"):
        folder_to_process = evidence_no_quotes
        process_folder(folder_to_process, export_file, outfile, outfile_error, now)
    elif(item_to_process =="EnCase Logical Evidence File"):
        file_to_process = evidence
        mount_point = mount_encase_v6_l01(case_number, file_to_process, outfile)
        process_folder(mount_point, export_file, outfile, outfile_error, now)

        #umount
        if(os.path.exists(mount_point)):
            subprocess.call(['sudo umount -f ' + mount_point], shell=True)
            os.rmdir(mount_point)
    elif(item_to_process == "Bit-Stream Image"):

        #set Mount Point
        mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")

        Image_Path = evidence

        #check if Image file is in Encase format
        if re.search(".E01", Image_Path):
            #set mount point
            #mount_point = "/mnt/"+	case_number+"_ewf"
            Image_Path = mount_ewf(Image_Path, outfile, mount_point)


        #call mmls function
        partition_info_dict, temp_time = mmls(outfile, Image_Path)
        partition_info_dict_temp = partition_info_dict

        #get filesize of mmls_output.txt
        file_size = os.path.getsize("/tmp/mmls_output_" + temp_time +".txt")

        #if filesize of mmls output is 0 then run parted
        if(file_size == 0):
            print("mmls output was empty, running parted\n")
            outfile.write("mmls output was empty, running parted\n")
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
            mmls_output_file.close()

        #loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
        for key,value in partition_info_dict.items():
            cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false"
            try:
                subprocess.call([cmd_false], shell=True)
            except:
                print("Autmount false failed")

            #process plist files
            if(value =="hfs+"):
                #call mount sub-routine
                success_code, loopback_device_mount = mount(value,str(key),Image_Path, outfile, mount_point)

                if(success_code):
                    print("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
                    outfile.write("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
                else:

                    print("We just mounted filesystem: " + value + " at offset:" + str(key) + "\n")
                    outfile.write("We just mounted filesystem: " + value + " at offset:" + str(key) + "\n")

                    #process
                    process_folder(mount_point, export_file, outfile, outfile_error, now)

                    #unmount
                    subprocess.call(['umount ' + mount_point], shell=True)
                    subprocess.call(['losetup -d ' + loopback_device_mount], shell=True)

            else:
                print("This partition is not formatted HFS+")
                outfile.write("This partition is not formatted HFS+\n\n")
        #close export_file
        export_file.close()


        #chdir to output foler
        os.chdir(folder_path)

        #unmount and remount points
        if re.search(".E01", Image_Path):
            if(os.path.exists(mount_point+"_ewf")):
                subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
                os.rmdir(mount_point+"_ewf")

        #remove empty directories
        for root, dirs, files in os.walk(folder_path, topdown = False):
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                if not os.listdir(dir_path):
                    outfile.write("Removing empty folder: " + dir_path + "\n")
                    os.rmdir(dir_path)

        #close outfiles
        outfile.close()

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

        #delete /tmp/ls_output.txt
        if (os.path.exists("/tmp/mmls_output_" + temp_time + ".txt")):
            os.remove("/tmp/mmls_output_" + temp_time + ".txt")
        if (os.path.exists("/tmp/timeline_partition_info_" + temp_time +".txt")):
            os.remove("/tmp/timeline_partition_info_" + temp_time +".txt")
        if (os.path.exists("/tmp/dump_" + temp_time + ".txt")):
            os.remove("/tmp/dump_" + temp_time + ".txt")
        if (os.path.exists("/tmp/fls_output_" + temp_time + ".txt")):
            os.remove("/tmp/fls_output_" + temp_time + ".txt")
        if (os.path.exists("/tmp/hives_to_rename_" + temp_time)):
            shutil.rmtree("/tmp/hives_to_rename_" + temp_time)



        #return(folder_path)
