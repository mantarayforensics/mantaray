### MOUNT PARTITIONS ##########################################################################################
#DESCRIPTION: This module mounts a partition
#INPUT: Filesystem, offset, absolute path to image, logfile location ("NONE" if logging is not required), and mount_point location
#OUTPUT: Returns success code (0 = mounted successfully, 1 = couldn't mount)

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

import subprocess
import os



def mount(value,key,Image, outfile, mount_point):

	#initialize variables
	loopback_device_mount = "NONE"

	#check to see if /mnt/windows_mount is mounted
	grep_command = "mount | grep " + mount_point
	grep_result = subprocess.call([grep_command], shell=True)
	
	if(grep_result):
		print(mount_point + " is not mounted", end = "\n\n")
		if(outfile != "NONE"):
			outfile.write(mount_point + " is not mounted\n")
	else: 
		print (mount_point + " is mounted, will now unmount", end = "\n\n")
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
			outfile.write("Just created mount point: " + mount_point + "\n")
	else:
		print("Mount Point: " + mount_point + " already exists.")
		if(outfile != "NONE"):
			outfile.write("Mount Point: " + mount_point + " already exists.\n")

	#convert filesystem variable to correct format for mount command
	print("Filesystem is: " + value)
	if(value =="ntfs") or (value=="hpfs"):
		filesystem_mount = "ntfs-3g"
	elif(value=="fat32"):
		filesystem_mount = "vfat"
	elif(value=="fat16"):
		filesystem_mount = "msdos"
	elif(value=="fat"):
		filesystem_mount = "msdos"
	elif(value =="hfs+"):
		filesystem_mount = "hfsplus"
	elif(value =="ext"):
		filesystem_mount = "ext"
	elif(value =="Apple"):
		filesystem_mount = "hfsplus"
	elif(value =="hfsx"):
		filesystem_mount = "hfsplus"
	else: filesystem_mount = value

	#set up mount command
	if(filesystem_mount == "ntfs-3g"):
		mount_command = "mount -t "+ filesystem_mount + " -o loop,ro,show_sys_files,streams_interface=windows,offset=" + str(key) +" " + Image +" " + mount_point
	elif(filesystem_mount == "ext"):
		mount_command = "mount -t " + filesystem_mount + " -o loop,ro,noexec,noload,offset=" + str(key) + " " + Image + " " + mount_point
	elif(filesystem_mount == "hfsplus"):
		#under 3.x kernel we need to use losetup when attempting to mount hfs+ partitions within disk images

		#use parted to get size of partition
		parted_command = "echo unit B print q | parted " + Image + " | grep " + key + " | grep hfs+ | awk '{print $4}' | sed s/B//"
		partition_size = subprocess.check_output([parted_command], shell=True)

		#decode partition size
		partition_size = partition_size.decode(encoding='UTF-8')
		partition_size = partition_size.strip()

		#set up loopback
		#losetup_command = "losetup --offset " + str(key) + " --sizelimit " + str(partition_size) + " -r /dev/loop7 " + Image
		losetup_command = "losetup --offset " + str(key) + " --sizelimit " + str(partition_size) + " -r -f " + Image
		print("The losetup command is: " + losetup_command)
		subprocess.call([losetup_command], shell=True)

		#check to see which loopback device we want to mount
		losetup_a_command = "losetup -a | grep " + str(partition_size) + " | awk '{print $1}' | sed s/://"
		loopback_device_to_mount = subprocess.check_output([losetup_a_command], shell=True)
		loopback_device_mount = loopback_device_to_mount.decode(encoding='UTF-8')
		loopback_device_mount = loopback_device_mount.strip()

		print("The loopback device to mount is: " + loopback_device_mount)

		#mount loopback device
		mount_command = "mount -t hfsplus -o ro " + loopback_device_mount + " " + mount_point
	elif(filesystem_mount != ""):
		mount_command = "mount -t " + filesystem_mount + " -o loop,ro,offset=" + str(key) + ",noexec,noatime,nodiratime " + Image + " " + mount_point	
	else:
		mount_command = "mount -o loop,ro,offset=" + str(key) + " " + Image + " " + mount_point
	
	#print out the mount command for debugging purposes
	print("*********************************************************************")
	print ("The mount command is: " + mount_command)
	print("*********************************************************************",end = "\n\n")

	if(outfile != "NONE"):
		outfile.write("*********************************************************************\n")
		outfile.write("The mount command is: " + mount_command + "\n")
		outfile.write("*********************************************************************\n\n")

	#run the mount command
	success = subprocess.call([mount_command], shell=True)

	return success, loopback_device_mount
		
		
		
	

### MOUNT PARTITIONS ###
