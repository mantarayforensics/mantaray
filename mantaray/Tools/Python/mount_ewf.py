### MOUNT_EWF ##################################################################################
#DESCRIPTION: This module calls mount_ewf.py to mount an Encase Image to /mnt/ewf
#INPUT: Absolute path to image file you want to mount, logfile location ("NONE" if you don't want to log events)
#OUTPUT: absolute path to virtual image file created by mount_ewf.py surrounded by single quotes (ex: '/mnt/ewf/dell_laptop')

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

import os
import subprocess


def mount_ewf(Image_Path, outfile, mount_point):

    #get the filename without extension
    fileName, fileExtension = os.path.splitext(Image_Path)
    file_name = os.path.basename(fileName)

    print("The file extension is: " + str(fileExtension))
    print("The file Name is: " + file_name)

    if(outfile != "NONE"):
        outfile.write("The file extension is: " + str(fileExtension) + "\n")
        outfile.write("The file Name is: " + file_name + "\n\n")

    #add ewf to the mount point passed into this function
    ewf_mount_point = mount_point + "_ewf"

    #check to see if mount_point_ewf is mounted
    grep_command = "mount | grep " + ewf_mount_point
    grep_result = subprocess.call([grep_command], shell=True)

    if(grep_result):
        print(ewf_mount_point + " is not mounted\n\n")
        if(outfile != "NONE"):
            outfile.write(ewf_mount_point + " is not mounted\n")
    else:
        print (ewf_mount_point + " is mounted, will now unmount\n\n")
        if(outfile != "NONE"):
            outfile.write(ewf_mount_point + " is mounted, will now unmount\n")
        #setup unmount command
        unmount_command = "umount -f " + ewf_mount_point
        subprocess.call([unmount_command], shell=True)

    #check to see if the folder exists, if not create it
    if not os.path.exists(ewf_mount_point):
        os.makedirs(ewf_mount_point)
        print("Just created mount point: " + ewf_mount_point)
        if(outfile != "NONE"):
            outfile.write("Just created mount point: " + ewf_mount_point)
    else:
        print("Mount Point: " + ewf_mount_point + " already exists.")
        if(outfile != "NONE"):
            outfile.write("Mount Point: " + ewf_mount_point + " already exists.")

    #umount /mnt/ewf just in case
    subprocess.call(['sudo umount ' + ewf_mount_point], shell=True)

    #mount the E01
    #mount_ewf_command = "mount_ewf.py "  + Image_Path  + " " + ewf_mount_point
    mount_ewf_command = "ewfmount " + Image_Path + " " + ewf_mount_point
    print("The mount_ewf command is: " + mount_ewf_command)
    outfile.write("The mount_ewf command is: " + mount_ewf_command)

    # disable auto-mount in nautilis - this stops a nautilis window from popping up everytime the mount command is executed
    cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && " \
                "sudo gsettings set org.gnome.desktop.media-handling automount-open false && " \
                "sudo gsettings set org.gnome.desktop.media-handling automount-never true"
    try:
        subprocess.call([cmd_false], shell=True)
    except:
        print("Autmount false failed")

    subprocess.call([mount_ewf_command], shell=True)


    #add quotes to image path in case of spaces
    quoted_path = "'" + ewf_mount_point + "/" + "ewf1" +"'"
    return quoted_path


### MOUNT_EWF ##################################################################################
