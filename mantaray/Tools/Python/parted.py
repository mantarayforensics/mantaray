### RUN PARTED COMMAND TO PARSE PARTITION TABLE ####################################################################
#DESCRIPTION: This module runs the parted command against the image file selected
#INPUT: This modules takes the logfile location (or NONE if logging is not required) and the absolute path to the image file to run parted against
#OUTPUT: This module returns a dictionary containing the partition info for the entire drive (key=offset, value=filesystem) 

##########################COPYRIGHT INFORMATION############################
# Copyright (C) 2014 webmaster@mantarayforensics.com 					  #
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
import io
import sys
import string
import subprocess
import datetime


def parted(outfile, Image_Path):
    #initialize variables
    partition_table = "NONE"
    partition_info_dict = {}

    #get datetime
    now = datetime.datetime.now()

    #get time for temp file to make it unique
    temp_time = now.strftime("%Y-%m-%d_%H_%M_%S_%f")

    #create string to print partition information
    # print_partition = "echo unit B print q"

    #set up parted command
    # parted = "parted " + Image_Path + " unit B print" # Commented out since unused
    parted_output = "sudo parted " + Image_Path + " unit B print > /tmp/timeline_partition_info_" + temp_time + ".txt"

    #run parted and collect output in tmp folder
    print('Running parted to scan partition information...')
    subprocess.call([parted_output], shell=True)

    #setup print statement
    print("************** PARTITION INFORMATION *******************************************")
    if(outfile != "NONE"):
        outfile.write("************** PARTITION INFORMATION *******************************************\n")

    fh = open('/tmp/timeline_partition_info_' + temp_time +'.txt')

    for line in fh:
        if re.search('Error', line):
            print("Error: Parted could not mount " + Image_Path)
            break

        #write entire partition table out to log file
        outfile.write(line)
        #determine the partition table type
        if re.search("Partition Table: msdos", line):
            partition_table = "msdos"
            print ("The partition table is: msdos")
            if(outfile != "NONE"):
                outfile.write("The partition table is: msdos\n")
        elif re.search("Partition Table: gpt", line):
            partition_table = "gpt"
            print ("The partition table is: gpt")
            if(outfile != "NONE"):
                outfile.write("The partition table is: gpt\n")
        elif re.search("Partition Table: loop", line):
            partition_table = "loop"
            print ("The partition table is: loop")
            if(outfile != "NONE"):
                outfile.write("The partition table is: loop\n")
        elif re.search("Partition Table: mac", line):
            partition_table = "mac"
            print ("The partition table is: mac")
            if(outfile != "NONE"):
                outfile.write("The partition table is: mac\n")

        #figure out which line contains the partition info we care about (line begins with a space and then a number)
        if(re.search('^\x20\d',line)) or (re.search('^\d{1}',line)):
            if(re.search('extended',line)):
                print("Skip the extended partition")
                if(outfile != "NONE"):
                    outfile.write("Skip the extended partition\n")
            else:
                sys.stdout.write(line)

                #split data from parted on spaces
                parted_data_list = line.split()

                #capture the starting offset for the partition
                partition_start = parted_data_list[1]

                #remove the trailing B from the parted output
                partition_start = partition_start[:-1]

                #capture the filesystem for the partition
                if (partition_table == "gpt"):
                    partition_filesystem = parted_data_list[4]
                elif (partition_table == "loop"):
                    partition_filesystem = parted_data_list[4]
                elif (partition_table == "mac"):
                    partition_filesystem = parted_data_list[4]
                elif (partition_table == "msdos"):
                    partition_filesystem = parted_data_list[5]

                if (re.search('linux-swap', partition_filesystem)):
                    print("Skipping the linux-swap partition")
                    if(outfile != "NONE"):
                        outfile.write("Skipping the linux-swap partition\n")
                else:
                    #push partition information into a dictionary for later use
                    partition_info_dict[partition_start] = partition_filesystem

    # Skip partition if no partition found
    if partition_table == "None":
        print("Error: Skipping image " + Image_Path + " since the partition table cannot be parsed")
        return None, temp_time

    #loop through the dictionary and print out the values for this partition
    # filesystem = value, partition_start = key
    for key,value in partition_info_dict.items():
        print("A filesystem to process is: " + value)
        print("The partition starts at offset: " + key)
        if(outfile != "NONE"):
            outfile.write("\nLooping through the dictionary holding the partition info\n")
            outfile.write("A filesystem to process is: " + value + "\n")
            outfile.write("The partition starts at offset: " + key + "\n")
    print("************** PARTITION INFORMATION *******************************************\n\n")

    if (outfile):
        outfile.write("************** PARTITION INFORMATION *******************************************\n\n")

    outfile.write("\n")
    #exit if partition table is not recognized
    # if partition_table == "NONE":
    #     print("Exiting program since partition table on this image is not recognized")
    #     sys.exit(0)

    #close fh
    fh.close()




    #return dictionary containing the partition information for the entire drive
    return partition_info_dict, temp_time

### RUN PARTED COMMAND TO PARSE PARTITION TABLE ###

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parse partition table of a raw image", epilog="Used in the MantaRay Suite. Learn more at http://mantarayforensics.com")
    parser.add_argument('image', help="path to image file to parse")
    parser.add_argument('log', help='output file to write log to', default="None")
    args = parser.parse_args()

    part_info, temp_time = parted(open(args.log, 'w'), args.image)

    import pprint
    print("Partition Details")
    pprint.pprint(part_info)