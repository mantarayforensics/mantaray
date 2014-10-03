#!/usr/bin/env python3
#Recurses an entire image file locates files that may contain data of interest

#import modules
from easygui import *
from get_case_number import *
from get_output_location import *
from select_file_to_process import *
from select_folder_to_process import *
from parted import *
from mmls import *
from mount import *
from mount_ewf import *
from done import *
from unix2dos import *
from convert_dms_to_decimal import *
from check_for_folder import *
from mount_encase_v6_l01 import *

import os
import re
import io
import sys
import string
import subprocess
import shutil
import simplekml
import datetime

### PROCESS SINGLE FILE #########################################################################################################


def process_single_file(evidence, outfile, folder_path, key, outfile3):

    #initialize variables
    lat_long = []
    files_of_interest = {}
    files_of_interest_list = []

    #get file extension
    fileName, fileExtension = os.path.splitext(evidence)
    print("The filename is: " + fileName)
    print("The fileext is: " + fileExtension)
    filenames = fileName + fileExtension
    quoted_full_path = '"' + evidence + '"'
    if(fileExtension.lower() == ".jpg") or (fileExtension.lower() == ".jpeg"):
        exiftool_command = "exiftool -ext " + fileExtension.lower() + " " + quoted_full_path + " | grep 'GPS Position'"
        result = subprocess.call([exiftool_command], shell=True)
        if(result):
            print("No GPS Data in file: " + filenames)
        else:
            #create output folder for processed files
            check_for_folder(folder_path + "/Processed_files_" + str(key), outfile)
            check_for_folder(folder_path + "/Processed_files_" + str(key) + "/GPS_DATA", outfile)

            #check to see if kml file exists
            if(os.path.isfile(folder_path + "/Processed_files_" +str(key) +"/GPS_DATA/" + "GPS_EXIF_data.kml")):
                print("KML file already exists")
            else:
                #chdir to output folder
                os.chdir(folder_path + "/Processed_files_" + str(key) + "/GPS_DATA")
                kml = simplekml.Kml()

            #copy file with exifdata to output folder
            #shutil.copyfile(evidence, folder_path + "/Processed_files_" + str(key) + "/GPS_DATA/" + filenames)

            #call exiftool again and capture the lat long information into a list
            (longitude, latitude) = convert_dms_to_decimal(quoted_full_path, fileExtension.lower())
            print("The latitude is: " + str(latitude))
            print("The longitude is: " + str(longitude))


            if not(longitude == "NULL") and not (latitude =="NULL"):
                #add data to kml file
                kml.newpoint(name=filenames, coords=[(latitude, longitude)])

                #save kml file
                kml.save("GPS_EXIF_data.kml")

                #add filename to list
                files_of_interest_list.append(filenames)

                #get filesize
                file_size = os.path.getsize(evidence)
                file_size = int(file_size)//1024
                #calculate MD5 value of file
                md5value = subprocess.check_output(["md5sum " + quoted_full_path + "| awk '{print $1}'"], shell=True, universal_newlines=True)
                md5value = md5value.strip()
                outfile3.write(quoted_full_path + "\t" + md5value + "\t" + str(file_size) + "\n")


#################################################################################################################################

### PROCESS ######################################################################################################################


def process(mount_point, outfile, folder_path, key, outfile3):

    #initialize variables
    lat_long = []
    files_of_interest = {}
    files_of_interest_list = []

    #create output folder for processed files if it doesn't exist
    if not os.path.exists(folder_path + "/Processed_files_" + str(key)):
        os.mkdir(folder_path + "/Processed_files_" + str(key))


    #scan directory tree for files of interest
    for root, dirs, files in os.walk(mount_point):
        for filenames in files:
            #get file extension
            fileName, fileExtension = os.path.splitext(filenames)
            full_path = os.path.join(root,filenames)
            quoted_full_path = '"' +full_path+ '"'
            if(fileExtension.lower() == ".jpg") or (fileExtension.lower() == ".jpeg"):
                exiftool_command = "exiftool -ext " + fileExtension.lower() + " " + quoted_full_path + " | grep 'GPS Position'"
                result = subprocess.call([exiftool_command], shell=True)
                if(result):
                    print("No GPS Data in file: " + filenames)
                else:
                    if not os.path.exists(folder_path + "/Processed_files_" + str(key) + "/GPS_DATA"):
                        os.mkdir(folder_path + "/Processed_files_" + str(key) + "/GPS_DATA")

                    #check to see if kml file exists
                    if(os.path.isfile(folder_path + "/Processed_files_" +str(key) +"/GPS_DATA/" + "GPS_EXIF_data.kml")):
                        print("KML file already exists")
                    else:
                        #chdir to output folder
                        os.chdir(folder_path + "/Processed_files_" + str(key) + "/GPS_DATA")
                        kml = simplekml.Kml()

                    #copy file with exifdata to output folder
                    shutil.copyfile(full_path, folder_path + "/Processed_files_" + str(key) + "/GPS_DATA/" + filenames)

                    #call exiftool again and capture the lat long information into a list
                    (longitude, latitude) = convert_dms_to_decimal(quoted_full_path, fileExtension.lower())
                    print("The latitude is: " + str(latitude))
                    print("The longitude is: " + str(longitude))


                    #add data to kml file
                    kml.newpoint(name=filenames, coords=[(latitude, longitude)])

                    #save kml file
                    kml.save("GPS_EXIF_data.kml")

                    #add filename to list
                    files_of_interest_list.append(filenames)

                    #get filesize
                    file_size = os.path.getsize(full_path)
                    file_size = int(file_size)//1024
                    #calculate MD5 value of file
                    md5value = subprocess.check_output(["md5sum " + quoted_full_path + "| awk '{print $1}'"], shell=True, universal_newlines=True)
                    md5value = md5value.strip()
                    outfile3.write(quoted_full_path + "\t" + md5value + "\t" + str(file_size) + "\n")
### PROCESS ######################################################################################################################


def unique(list):
    y = []
    for x in list:
        if x not in y:
            y.append(x)
    return y

## MAIN PROGRAM ####################################################################################################################

def create_kml_from_exif_mr(item_to_process, case_number, root_folder_path, evidence):
    print("The item to process is: " + item_to_process)
    print("The case_name is: " + case_number)
    print("The output folder is: " + root_folder_path)
    print("The evidence to process is: " + evidence)

    evidence_no_quotes = evidence
    evidence = '"' + evidence + '"'

    #create output folder path
    folder_path = root_folder_path + "/" + "KML_From_EXIF"
    check_for_folder(folder_path, "NONE")


    #open a log file for output
    log_file = folder_path + "/KML_From_EXIF_logfile.txt"
    outfile = open(log_file, 'wt+')

    #initialize variables
    files_of_interest = {}
    files_of_interest_list = []
    mount_point = "NONE"

    log_file3 = folder_path + "/" + case_number + "_files_to_exploit.xls"
    outfile3 = open(log_file3, 'wt+')

    #write out column headers to xls file
    outfile3.write("Name\tMD5\tFile Size (kb)\n")



    if(item_to_process == "Directory"):
        #select folder to process
        folder_process = evidence_no_quotes

        #set folder variable to "folder" since this is a folder and not a disk partition
        folder = "Directory"

        #call process subroutine
        process(folder_process, outfile, folder_path, folder, outfile3)

    elif(item_to_process == 'EnCase Logical Evidence File'):
        folder = "LEF"
        file_to_process = evidence
        mount_point = mount_encase_v6_l01(case_number, file_to_process, outfile)
        process(mount_point, outfile, folder_path, folder, outfile3)

        #umount
        if(os.path.exists(mount_point)):
            subprocess.call(['sudo umount -f ' + mount_point], shell=True)
            os.rmdir(mount_point)

    elif(item_to_process == 'Single File'):
        process_single_file(evidence_no_quotes, outfile, folder_path, "Single-File", outfile3)

    elif(item_to_process == 'Bit-Stream Image'):

        #select image to process
        Image_Path = evidence

        #get datetime
        now = datetime.datetime.now()

        #set Mount Point
        mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S")

        #check to see if Image file is in Encase format
        if re.search(".E01", Image_Path):
            #strip out single quotes from the quoted path
            no_quotes_path = Image_Path.replace("'","")
            print("The no quotes path is: " + no_quotes_path)
            #call mount_ewf function
            cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false"
            try:
                subprocess.call([cmd_false], shell=True)
            except:
                print("Automount false failed")
            Image_Path = mount_ewf(Image_Path, outfile, mount_point)

        #call mmls function
        partition_info_dict, temp_time = mmls(outfile, Image_Path)
        #partition_info_dict_temp, temp_time = partition_info_dict

        #get filesize of mmls_output.txt
        file_size = os.path.getsize("/tmp/mmls_output_" + temp_time +".txt")
        print("The filesize is: " + str(file_size))

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

            #close file
            mmls_output_file.close()

        #loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
        #for key,value in partition_info_dict.items():
        for key,value in sorted(partition_info_dict.items()):

            #create output folder for processed files
            if not os.path.exists(folder_path + "/Processed_files_" + str(key)):
                os.mkdir(folder_path + "/Processed_files_" + str(key))

            #disable auto-mount in nautilis - this stops a nautilis window from popping up everytime the mount command is executed
            cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false"
            try:
                subprocess.call([cmd_false], shell=True)
            except:
                print("Automount false failed")

            #call mount sub-routine
            success_code, loopback_device_mount = mount(value,key,Image_Path, outfile, mount_point)

            if(success_code):
                print("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
                outfile.write("Could not mount partition with filesystem: " + value + " at offset:" + str(key))
            else:

                print("We just mounted filesystem: " + value + " at offset:" + str(key) + ". Scanning for files of interest.....\n")
                outfile.write("We just mounted filesystem: " + value + " at offset:" + str(key) + "\n")

                #call process subroutine
                process(mount_point, outfile, folder_path, key, outfile3)


                #unmount and remove mount points
                if(os.path.exists(mount_point)):
                    subprocess.call(['sudo umount -f ' + mount_point], shell=True)
                    #os.rmdir(mount_point)
                #unmount loopback device if this image was HFS+ - need to run losetup -d <loop_device> before unmounting
                if not (loopback_device_mount == "NONE"):
                    losetup_d_command = "losetup -d " + loopback_device_mount
                    subprocess.call([losetup_d_command], shell=True)

            #delete /tmp files created for processing bit-stream images
            if (os.path.exists("/tmp/mmls_output_" + temp_time + ".txt")):
                os.remove("/tmp/mmls_output_" + temp_time + ".txt")

    #write out list of filenames to end of output file so that user can create a filter for those filenames in Encase
    outfile3.write("\n\n******** LIST of FILENAMES of INTEREST ******************\n")
    #sort list so that all values are unique
    unique(files_of_interest_list)
    for files in files_of_interest_list:
        outfile3.write(files + "\n")


    #program cleanup
    outfile.close()
    outfile3.close()

    #remove mount points created for this program
    if(os.path.exists(mount_point)):
        subprocess.call(['sudo umount -f ' + mount_point], shell=True)
        os.rmdir(mount_point)
    if(os.path.exists(mount_point+"_ewf")):
        subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
        os.rmdir(mount_point+"_ewf")

    #convert outfile using unix2dos
    #chdir to output foler
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
                unix2dos_command = "sudo unix2dos " + filenames
                subprocess.call([unix2dos_command], shell=True)

    #delete empty directories in output folder
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for directories in dirs:
            files = []
            dir_path = os.path.join(root,directories)
            files = os.listdir(dir_path)
            if(len(files) == 0):
                os.rmdir(dir_path)

    #unmount and remove mount points
    if(mount_point != "NONE"):
        if(os.path.exists(mount_point+"_ewf")):
            subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
            os.rmdir(mount_point+"_ewf")


