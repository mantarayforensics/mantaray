#check to see if folder exists.  If it does then add the date, if not then create it

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2014 dougkoster@hotmail.com				                 #
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
import datetime

def check_for_folder(path, outfile):
	if not os.path.exists(path):
		os.makedirs(path)
		#print("Just created folder: " + path)
		if(outfile != "NONE"):
			outfile.write("\nJust created output folder: " + path + "\n")
		folder = path
	else:
		print("\nOutput folder: " + path + " already exists - appending date/time.")
		#get datetime
		now = datetime.datetime.now()
		os.makedirs(path +"_" + now.strftime("%Y-%m-%d_%H_%M_%S"))
		if(outfile != "NONE"):
			outfile.write("Just created output folder: " + path +"_" + now.strftime("%Y-%m-%d_%H_%M_%S"))
		folder = path + "_" + now.strftime("%Y-%m-%d_%H_%M_%S")

	return folder
