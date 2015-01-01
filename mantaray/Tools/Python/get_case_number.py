### GET CASE ID ###
# DESCRIPTION: This module uses easygui to pop up a message box asking for the user to enter a case number
# INPUT: NONE
# OUTPUT: case_number

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
import sys


def get_case_number():
    #global case_number
    case_number = enterbox(msg="Please Enter Case Number", title='Case Number',default='',strip=True,image=None,root=None)
    if case_number == None:
        print ("Cancel chosen")
        sys.exit(0)
    if case_number == "":
        print ("Case number is missing.")
        sys.exit(0)

    #replace spaces with underscores
    case_number.replace(" ","_")
    return case_number

### GET CASE ID ###
