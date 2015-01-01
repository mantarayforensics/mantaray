#parse the final .csv file output from supertimeline script

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


#import modules
from csv import reader

from done import *



#get file to process
csv_file = fileopenbox(msg="Select File to Process",title="Select File",default='/mnt/hgfs/*.*')

#get output folder
#folder_path = diropenbox(msg="Output Location",title="Choose Path",default='/mnt/hgfs/')

#open csv file
infile = open(csv_file, 'rt+')

#open outfile
out_file = csv_file + "_timeline_modules.csv"
outfile = open(out_file, 'wt+')

#loop through file
infile.seek(0)

parser = reader(infile)


for record in parser:
    print(record[2])



