#parse the final .csv file output from supertimeline script

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



