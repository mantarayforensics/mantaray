### DONE ########################################################################################
#DESCRIPTION: This module pops up an easygui messagebox telling the user where the output files are located
#INPUT: absolut path to folder where output files are located
#OUTPUT: NONE

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


from share.Tools.Python.easygui import *


def done(folder_path):
	#create message box telling user where output is located
	msgbox(msg='Process Complete.  Your output is located in: ' + folder_path, title='Processing Complete ', ok_button='OK', image=None, root=None)
	


### DONE ########################################################################################
