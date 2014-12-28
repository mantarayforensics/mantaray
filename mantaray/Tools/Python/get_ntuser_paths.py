### GET NTUSER.DAT FILES ################################################################
#DESCRIPTION: This module finds the absolute path to each NTUSER.DAT file within a given mount point
#INPUT: absolute path to mount point (ex: "/mnt/windows_mount")
#OUTPUT: returns a list containing the absolute path to each NTUSER.DAT file found in that partition

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

import os

def get_ntuser_paths(mount_point):
    #initialize tuple
    nt_user_dat = []
    #root_string_length = 0
    #rightmost_slash_location = 0

    #get paths to all NTUSER.DAT files
    for root,dirs,files in os.walk(mount_point):
        for filenames in files:
            #if 'NTUSER.DAT' in filenames:
            if(filenames.endswith('NTUSER.DAT')) or (filenames.endswith('ntuser.dat')):
                #append the full path to each NTUSER.dat file to list nt_user_dat
                nt_user_dat.append(os.path.join(root,filenames))


    print("The user accounts are: *********************************************")
    for items in nt_user_dat:
        print (items)
    print("*********************************************************************\n\n")
    return (nt_user_dat)

### GET NTUSER.DAT FILES ####
