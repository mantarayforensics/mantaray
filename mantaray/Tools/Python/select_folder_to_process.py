#DESCRIPTION: This script uses easy gui to ask the user to select a folder
#INPUT: Absolute path to output log file
#OUTPUT: absolute path to a folder

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

from easygui import *


def select_folder_to_process(outfile):
    folder = diropenbox(msg='', title='Select Folder to Process', default='/mnt/hgfs/')

    #add quotes to image path in case of spaces
    quoted_path = "'" +folder +"'"

    if(outfile != "NONE"):
            outfile.write("Folder selected: " + quoted_path + "\n\n")

    return folder