#parse the final .csv file output from supertimeline script

#import modules
import re
import subprocess

from done import *



#get file to process
csv_file = fileopenbox(msg="Select File to Process",title="Select File",default='/mnt/hgfs/*.*')

#get output folder
folder_path = diropenbox(msg="Output Location",title="Choose Path",default='/mnt/hgfs/')

#open csv file
infile = open(csv_file, encoding='latin-1')
#infile = open(csv_file, 'r+')

#open outfile
out_file = csv_file + "_timeline_modules.csv"
outfile = open(out_file, 'wt+')

#skip header row
next(infile)

#loop through csv file
for line in infile:
    #split line on space
    #line_split = line.split(',')
    line_split = line.split(",",7)


    date_time = line_split[0]
    size = line_split[1]
    type1 = line_split[2]
    mode = line_split[3]
    uid = line_split[4]
    gid = line_split[5]
    meta = line_split[6]
    file_name = line_split[7]

    #remove " from file_name
    file_name1 = file_name.replace('"', '')

    if(re.search('^\\[', file_name1)):
        #print(line)

        #determine log2timeline module
        module_name = file_name.split(']')
        module_name1 = module_name[0].replace('[','')
        module_name1 = module_name[0].replace('"','')
        print("The module is: " + module_name1 + "]")

        #create new line for output file
        newline = date_time + ',' + size + "," + type1 + ',' + mode + ',' + uid + ',' + gid + ',' + meta + ',' + module_name1 + '],' + file_name
        outfile.write(newline)

    else:
        newline = date_time + ',' + size + "," + type1 + ',' + mode + ',' + uid + ',' + gid + ',' + meta + ',' +'' + ',' + file_name
        print("The module is: N/A")
        outfile.write(newline)
outfile.close()

#add header line back into modified supertimeline
sed_command = "sudo sed -i '1i\ Date,Size,Type,Mode,UID,GID,Meta,L2T_Function,File_Name' "  + "'"+ csv_file +"_timeline_modules.csv" + "'";
subprocess.call([sed_command], shell=True)

