#!/usr/bin/env python3
#This function mounts an Encase v6 .L01 image

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

import os
import subprocess
import datetime

def mount_encase_v6_l01(case_name, l01_file, outfile):
    print("Inside mount L01 function")

    #get datetime
    now = datetime.datetime.now()

    #get time for temp file to make it unique
    temp_time = now.strftime("%Y-%m-%d_%H_%M_%S_%f")

    #set Mount Point
    mount_point = "/mnt/" + temp_time

    #check to see if /mnt/windows_mount is mounted
    grep_command = "mount | grep " + mount_point
    grep_result = subprocess.call([grep_command], shell=True)

    if(grep_result):
        print(mount_point + " is not mounted\n\n")
        if(outfile != "NONE"):
            outfile.write(mount_point + " is not mounted\n")
    else:
        print (mount_point + " is mounted, will now unmount\n\n")
        if(outfile != "NONE"):
            outfile.write(mount_point + " is mounted, will now unmount\n")
        #setup unmount command
        unmount_command = "umount -f " + mount_point
        subprocess.call([unmount_command], shell=True)

    #check to see if the folder exists, if not create it
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)
        print("Just created mount point: " + mount_point)
        if(outfile != "NONE"):
            outfile.write("Just created mount point: " + mount_point)
    else:
        print("Mount Point: " + mount_point + " already exists.")
        if(outfile != "NONE"):
            outfile.write("Mount Point: " + mount_point + " already exists.")

    l01_mount_command = "ewfmount -f files " + l01_file + " " + mount_point

    #execute l01_mount_command
    subprocess.call([l01_mount_command], shell=True)

    return mount_point
