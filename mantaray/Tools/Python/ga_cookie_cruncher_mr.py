#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2014 Chapin.Bryce@Mantech.com				             #
#This program is free software: you can redistribute it and/or modify    #
#it under the terms of the GNU General Public License as published by    #
#the Free Software Foundation, either version 3 of the License, or       #
#(at your option) any later version.                                     #
#                                                                        #
#This program is distributed in the hope that it will be useful,         #
#but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#GNU General Public License for more details.                            #
#                                                                        #
#You should have received a copy of the GNU General Public License       #
#along with this program.  If not, see http://www.gnu.org/licenses/.     #
#########################COPYRIGHT INFORMATION############################
"""This script automates the use of ga_parser.py as released by Mari DeGrazia."""

__author__ = 'cbryce'

import subprocess
import os
from parted import *
from mount_ewf import *
from remove_dupes_module_noask import *
from mmls import *
from Windows_Time_Converter_module import *
from check_for_folder import *
import mount


def process_dir(input_dir, output_dir, parsers, type):
    print ("Building Command...")
    cmd = "sudo python /usr/share/mantaray/Tools/Python/ga_parser.py -d " + input_dir + " -o " + output_dir + ""

    # Select parsers.
    if "chrome" in parsers:
        cmd += " --chrome"
    if "firefox" in parsers:
        cmd += " --firefox"
    if "ie" or "internet explorer" in parsers:
        cmd += " --ie"
    if "apple" in parsers:
        cmd += " --apple"
    if "ewf" in parsers:
        cmd += " --ewf"
    if "gif" in parsers:
        cmd += " --gif"

    cmd += " --sigs "

    # Add Logging
    cmd += " > " + output_dir + "_" + type + "_logfile.txt"

    print("Command Built. \nExecuting: " + cmd)

    # Execute command.
    subprocess.call([cmd], shell=True)


def process_file(input_file, output_dir, parsers, type="Overt"):
    print ("Building Command...")
    cmd = "sudo python /usr/share/mantaray/Tools/Python/ga_parser.py -f " + input_file + " -o " + output_dir + ""

    # Select parsers.
    if "chrome" in parsers:
        cmd += " --chrome"
    if "firefox" in parsers:
        cmd += " --firefox"
    if "ie" or "internet explorer" in parsers:
        cmd += " --ie"
    if "apple" in parsers:
        cmd += " --apple"
    if "ewf" in parsers:
        cmd += " --ewf"
    if "chrome" in parsers:
        cmd += " --gif"

    # Add Logging
    cmd += " > " + output_dir + "_" + type + "_logfile.txt"

    print("Command Built. \nExecuting: " + cmd)

    # Execute command.
    subprocess.call([cmd], shell=True)


def get_block_size_mmls(Image_Path, outfile, temp_time):
    block_size = subprocess.check_output(['mmls -i raw ' + Image_Path + " | grep Units | "
                                                                        "awk '{print $4}' | sed s/-byte//"],
                                                                        shell=True, universal_newlines=True)
    block_size = block_size.strip()
    print("The block size is: " + str(block_size))
    outfile.write("The block size is: " + str(block_size) + "\n\n")
    return block_size


def get_block_size_parted(outfile, temp_time):
    block_size_command = "sudo cat /tmp/timeline_partition_info_" + temp_time +".txt | grep -a " + "'"+\
                         "Sector size"+"'" + " | awk {'print $4'} | sed s_B/.*__"

    outfile.write("The block_size command is: " + block_size_command + "\n")
    block_size = subprocess.check_output([block_size_command], shell=True, universal_newlines=True)
    block_size = block_size.strip()
    print("The block size is: " + str(block_size))
    outfile.write("The block size is: " + str(block_size) + "\n\n")
    return block_size


def mount_shadow_volumes(vssvolume_mnt, outfile, folder_path, temp_time, parsers):

    print("Vssvolume_mnt: " + vssvolume_mnt)

    #check for existence of folder
    vss_mount = check_for_folder("/mnt/vss_mount", outfile)

    vss_volumes = os.listdir(vssvolume_mnt)
    print(vss_volumes)
    for item in vss_volumes:
        print("Currently processing vss volume: " + item)
        #call parted function
        partition_info_dict, temp_time = parted(outfile, vssvolume_mnt + "/"+item)
        block_size = get_block_size_parted(outfile, temp_time)
        for key,value in partition_info_dict.items():
            print("About to process registry hives from: " + item)
            mount.mount(value,key,vssvolume_mnt+"/"+item,outfile,vss_mount)
            os.makedirs(folder_path+"/"+item)
            process_dir(vss_mount, folder_path+"/"+item, parsers,item)

    #unmounting vss volume
    if(vssvolume_mnt != "NULL"):
        try:
            print("Unmounting: " + vssvolume_mnt)
            outfile.write("Unmounting: " + vssvolume_mnt + "\n")
            subprocess.call(['sudo umount -f ' + vssvolume_mnt], shell=True)
            os.rmdir(vssvolume_mnt)
        except:
            print("Unable to unmount: " + vssvolume_mnt)
            outfile.write("Unable to unmount: " + vssvolume_mnt)


def check_for_shadow_volumes(Image_Path, key, block_size, outfile, folder_path, temp_time):

    #set shadow volume variables
    has_shadow_volumes = "NULL"
    vssvolume_mnt = "NULL"

    #divide offset by block size so it is in correct format for vshadowinfo
    key_bytes = int(key)//int(block_size)
    key_bytes_disk_offset = int(key) * int(block_size)
    image_no_quotes = Image_Path.replace("'","")
    print("\nChecking: " + Image_Path + " for shadow volumes")

    f = open('/tmp/dump_' + temp_time + '.txt', 'w+t')
    try:
        vshadow_info_command = "vshadowinfo -v -o " + str(key) + " " + Image_Path# + " > /tmp/dump.txt"
        #print("The vshadow_command is: " + vshadow_info_command)
        outfile.write("The vshadow_command is: " + vshadow_info_command)
        subprocess.call([vshadow_info_command], shell=True, stdout = f, stderr=subprocess.STDOUT)
        #vshadow_output = subprocess.check_output([vshadow_info_command], shell=True, stderr=subprocess.STDOUT)
        #f.close()

        f =open('/tmp/dump_' + temp_time + '.txt', 'rt')
        #print("try succedded")
        for line in f:
            line = line.strip()
            print(line)
            if (re.search("No Volume Shadow Snapshots found", line)):
                has_shadow_volumes = "NO"

        if(has_shadow_volumes != "NO"):
            print("Partition at offset: " + str(key_bytes) + " has shadow volumes.")
            outfile.write("Partition at offset: " + str(key_bytes) + " has shadow volumes.")

            #check for existence of folder
            vssvolume_mnt = check_for_folder("/mnt/vssvolume", outfile)

            #mount shadow volumes for partition
            mount_shadow_command = "sudo vshadowmount -o " + str(key) + " " + Image_Path + " " + vssvolume_mnt
            print("The mount_shadow_command is: " + mount_shadow_command)

            subprocess.call(["sudo vshadowmount -o " + str(key) + " " + Image_Path + " " + vssvolume_mnt], shell=True,
                            stderr=subprocess.STDOUT)

            #pass vssvolume mount point to mount_shadow_volume for mounting
            mount_shadow_volumes(vssvolume_mnt, outfile, folder_path, temp_time)

        elif(has_shadow_volumes == "NO"):
            print("Partition at offset: " + str(key) + " has no shadow volumes")

        f.close()

    except:
        print("The vshadow_info command for partition: " + str(key) + " failed")

    return vssvolume_mnt


def main(input_file, output_directory, parsers):
    now = datetime.datetime.now()
    Image_Path = input_file
    mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S_%f")
    folder_path = output_directory

    #process_file(input_file,folder_path,parsers,type="Overt", threads)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    outfile = open((output_directory+"/GA_Cookie_Logfile.txt"),'w')

    if os.path.isdir(input_file):
        process_dir()
    if os.path.isfile(input_file):
        # Analyze 100 Megabytes chunks of any raw file or EWF file
        # Process overt & deleted
        #process_file(input_file,output_directory,parsers)

        ## Start check for Shadow Volumes
        # check if Image file is in Encase format
        if re.search(".E01", input_file):
            #set mount point
            Image_Path = mount_ewf(Image_Path, outfile, mount_point)

        # call mmls function
        partition_info_dict, temp_time = mmls(outfile, Image_Path)
        partition_info_dict_temp = partition_info_dict

        #get filesize of mmls_output.txt
        file_size = os.path.getsize("/tmp/mmls_output_" + temp_time +".txt")

        #if filesize of mmls output is 0 then run parted
        if file_size == 0:
            print("mmls output was empty, running parted\n")
            outfile.write("mmls output was empty, running parted\n")
            #call parted function
            partition_info_dict, temp_time = parted(outfile, Image_Path)
            block_size = get_block_size_parted(outfile, temp_time)

        else:
            #get block_size since mmls was successful
            block_size = get_block_size_mmls(Image_Path, outfile, temp_time)

            #read through the mmls output and look for GUID Partition Tables (used on MACS)
            mmls_output_file = open("/tmp/mmls_output_" + temp_time + ".txt", 'r')
            for line in mmls_output_file:
                if re.search("GUID Partition Table", line):
                    print("We found a GUID partition table, need to use parted")
                    outfile.write("We found a GUID partition table, need to use parted\n")
                    #call parted function
                    partition_info_dict = parted(outfile, Image_Path)
            mmls_output_file.close()

        #loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
        for key, value in partition_info_dict.items():

            #process overt images
            if(value == "ntfs") or (value == "fat32"):
                if not os.path.exists(folder_path + "/Partition_" + str(key)):
                    os.makedirs(folder_path + "/Partition_" + str(key))
                    #print("Just created output folder: " + folder_path + "/Partition_" + str(key))
                    outfile.write("Just created output folder: " + folder_path + "/Partition_" + str(key) + "\n\n")
                else:
                    print("Output folder: " + folder_path + "/Partition_" + str(key) + " already exists")
                    outfile.write("Output folder: " + folder_path + "/Partition_" + str(key) + " already exists\n\n")
                # Process Deleted, and Unallocated
                #input("Image Name: "+  Image_Path + "\nFolder Path: " +folder_path+"/Partition_"+str(key))
                tmp_mnt = mount_point+"_"+str(key)+"_"+value
                mount.mount(value, key, Image_Path, outfile, tmp_mnt)
                #process_file(Image_Path, folder_path+"/Partition_"+str(key), parsers)
                # Process the mounted filesystem.
                process_dir(tmp_mnt, folder_path+"/Partition_"+str(key), parsers, "Overt")
                # Processes Shadow Volumes
                vss_mount = check_for_shadow_volumes(Image_Path, key, block_size, outfile, folder_path, temp_time)
                if not vss_mount == "NULL":
                    mount_shadow_volumes(vss_mount,outfile,folder_path,now,parsers)

            else:
                print("This partition is not formatted NTFS or FAT32")
                outfile.write("This partition is not formatted NTFS or FAT32\n\n")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Automate the ga_parser.py for MantaRay")
    parser.add_argument("-f", help="File or directory in")
    parser.add_argument("-o", help="Output Directory")
    parser.add_argument("-p", help="Comma separated list of parsers to run. Available parsers include chome, firefox, "
                                   "safari, ie, gif")
    parser.add_argument("--ewf", help="Enable for EWF file inputs", action="store_true")
    # parser.add_argument("--threads", help="Select number of threads to use", type=int, action="store_true")
    args = parser.parse_args()

    parser_array = []
    for item in args.p.split(","):
        parser_array.append(item)

    if not parser_array:
        print("Please select at least 1 parser to run the tool.")

    if args.ewf:
        parser_array.append("ewf")

    if not os.path.exists(args.o):
        os.makedirs(args.o)

    main(input_file=args.f,output_directory=args.o,parsers=parser_array)