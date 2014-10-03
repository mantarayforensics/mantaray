#!/usr/bin/env python3
#Recurses an entire image file locates files that may contain data of interest

#import modules
import shutil

from get_case_number import *
from get_output_location import *
from select_file_to_process import *
from select_folder_to_process import *
from parted import *
from mmls import *
from mount import *
from mount_ewf import *
from done import *
from convert_dms_to_decimal import *
import simplekml


def process(mount_point, outfile, folder_path, key):

    #initialize variables
    lat_long = []

    #scan directory tree for files of interest
    for root, dirs, files in os.walk(mount_point):
        for filenames in files:
            #get file extension
            fileName, fileExtension = os.path.splitext(filenames)
            full_path = os.path.join(root,filenames)
            quoted_full_path = '"' +full_path+ '"'
            if(fileExtension.lower() == ".jpg") or (fileExtension.lower() == ".jpeg"):
                exiftool_command = "exiftool -ext " + fileExtension.lower() + " " + quoted_full_path + " | grep 'GPS Position'"
                result = subprocess.call([exiftool_command], shell=True)
                if(result):
                    print("No GPS Data in file: " + filenames)
                else:
                    #create output folder for processed files
                    if not os.path.exists(folder_path + "/Processed_files_" + str(key) + "/GPS_DATA"):
                        os.mkdir(folder_path + "/Processed_files_" + str(key) + "/GPS_DATA")

                    #check to see if kml file exists
                    if(os.path.isfile(folder_path + "/Processed_files_" +str(key) +"/GPS_DATA/" + "GPS_EXIF_data.kml")):
                        print("KML file already exists")
                    else:
                        #chdir to output folder
                        os.chdir(folder_path + "/Processed_files_" + str(key) + "/GPS_DATA")
                        kml = simplekml.Kml()

                    #copy file with exifdata to output folder
                    shutil.copyfile(full_path, folder_path + "/Processed_files_" + str(key) + "/GPS_DATA/" + filenames)

                    #call exiftool again and capture the lat long information into a list
                    (longitude, latitude) = convert_dms_to_decimal(quoted_full_path, fileExtension.lower())
                    print("The latitude is: " + str(latitude))
                    print("The longitude is: " + str(longitude))


                    #add data to kml file
                    kml.newpoint(name=filenames, coords=[(latitude, longitude)])

                    #save kml file
                    kml.save("GPS_EXIF_data.kml")

                    #add filename to list
                    files_of_interest_list.append(filenames)

                    #get filesize
                    file_size = os.path.getsize(full_path)
                    file_size = int(file_size)//1024
                    #calculate MD5 value of file
                    md5value = subprocess.check_output(["md5sum " + quoted_full_path + "| awk '{print $1}'"], shell=True, universal_newlines=True)
                    md5value = md5value.strip()
                    outfile3.write(quoted_full_path + "\t" + md5value + "\t" + str(file_size) + "\n")


def unique(list):
    y = []
    for x in list:
        if x not in y:
            y.append(x)
    return y

#initialize variables
files_of_interest = {}
files_of_interest_list = []
mount_point = "NONE"

#get case number
case_number = get_case_number()

#get output location
folder_path = get_output_location(case_number)

#open a log file for output
log_file = folder_path + "/" + case_number + "_logfile.txt"
outfile = open(log_file, 'wt+')
log_file3 = folder_path + "/" + case_number + "_files_to_exploit.xls"
outfile3 = open(log_file3, 'wt+')

#write out column headers to xls file
outfile3.write("Name\tMD5\tFile Size (kb)\n")

#ask user whether they want to process a single file on entire driv
process_choice = buttonbox(msg='What would you like to scan?', title='AV Scanning', choices=('Folder', 'Entire Disk Image'), image=None, root=None)

if(process_choice == "Folder"):
    #select folder to process
    folder_process = select_folder_to_process(outfile)

    #create output folder for processed files
    if not os.path.exists(folder_path + "/Processed_files_FOLDER"):
        os.mkdir(folder_path + "/Processed_files_FOLDER")

    #set folder variable to "folder" since this is a folder and not a disk partition
    folder = "FOLDER"

    #call process subroutine
    process(folder_process, outfile, folder_path, folder)

else:

    #select image to process
    Image_Path = select_file_to_process(outfile)
    print("The image path is: " + Image_Path)

    #get datetime
    now = datetime.datetime.now()

    #set Mount Point
    mount_point = "/mnt/" + now.strftime("%Y-%m-%d_%H_%M_%S")

    #check to see if Image file is in Encase format
    if re.search(".E01", Image_Path):
        #strip out single quotes from the quoted path
        no_quotes_path = Image_Path.replace("'","")
        print("The no quotes path is: " + no_quotes_path)
        #call mount_ewf function
        Image_Path = mount_ewf(Image_Path, outfile, mount_point)

    #call mmls function
    partition_info_dict = mmls(outfile, Image_Path)
    partition_info_dict_temp = partition_info_dict

    #get filesize of mmls_output.txt
    file_size = os.path.getsize("/tmp/mmls_output.txt")
    print("The filesize is: " + str(file_size))

    #if filesize of mmls output is 0 then run parted
    if(file_size == 0):
        print("mmls output was empty, running parted")
        outfile.write("mmls output was empty, running parted")
        #call parted function
        partition_info_dict = parted(outfile, Image_Path)

    else:

        #read through the mmls output and look for GUID Partition Tables (used on MACS)
        mmls_output_file = open("/tmp/mmls_output.txt", 'r')
        for line in mmls_output_file:
            if re.search("GUID Partition Table", line):
                print("We found a GUID partition table, need to use parted")
                outfile.write("We found a GUID partition table, need to use parted\n")
                #call parted function
                partition_info_dict = parted(outfile, Image_Path)

    #loop through the dictionary containing the partition info (filesystem is VALUE, offset is KEY)
    #for key,value in partition_info_dict.items():
    for key,value in sorted(partition_info_dict.items()):

        #create output folder for processed files
        if not os.path.exists(folder_path + "/Processed_files_" + str(key)):
            os.mkdir(folder_path + "/Processed_files_" + str(key))

        #disable auto-mount in nautilis - this stops a nautilis window from popping up everytime the mount command is executed
        cmd_false = "sudo gsettings set org.gnome.desktop.media-handling automount false && sudo gsettings set org.gnome.desktop.media-handling automount-open false"
        try:
            subprocess.call([cmd_false], shell=True)
        except:
            print("Autmount false failed")

        #call mount sub-routine
        success_code = mount(value,key,Image_Path, outfile, mount_point)

        if(success_code):
            print("Could not mount partition with filesystem: " + value + " at offset:" + key)
            outfile.write("Could not mount partition with filesystem: " + value + " at offset:" + key)
        else:

            print("We just mounted filesystem: " + value + " at offset:" + str(key) + ". Scanning for files of interest.....\n")
            outfile.write("We just mounted filesystem: " + value + " at offset:" + str(key) + "\n")

        #call process subroutine
        process(mount_point, outfile, folder_path, key)


        #call mount sub-routine
        print("Unmounting mount point before exiting\n\n")
        outfile.write("Unmounting mount point before exiting\n\n")
        subprocess.call(['umount ' + mount_point], shell=True)

#write out list of filenames to end of output file so that user can create a filter for those filenames in Encase
outfile3.write("\n\n******** LIST of FILENAMES of INTEREST ******************\n")
#sort list so that all values are unique
unique(files_of_interest_list) 
for files in files_of_interest_list:
    outfile3.write(files + "\n")


#program cleanup
outfile.close()
outfile3.close()
#convert outfile using unix2dos	
#chdir to output foler
os.chdir(folder_path)

#run text files through unix2dos
for root, dirs, files in os.walk(folder_path):
        for filenames in files:
            #get file extension
            fileName, fileExtension = os.path.splitext(filenames)
            if(fileExtension.lower() == ".txt"):
                full_path = os.path.join(root,filenames)
                quoted_full_path = "'" +full_path+"'"
                print("Running Unix2dos against file: " + filenames)
                unix2dos_command = "sudo unix2dos " + filenames
                subprocess.call([unix2dos_command], shell=True)

#delete empty directories in output folder
for root, dirs, files in os.walk(folder_path, topdown=False):	
    for directories in dirs:
        files = []
        dir_path = os.path.join(root,directories)
        files = os.listdir(dir_path)
        if(len(files) == 0):
            os.rmdir(dir_path)

#unmount and remove mount points
if(mount_point != "NONE"):
    if(os.path.exists(mount_point)):
        subprocess.call(['sudo umount -f ' + mount_point], shell=True)
        os.rmdir(mount_point)
    if(os.path.exists(mount_point+"_ewf")):
        subprocess.call(['sudo umount -f ' + mount_point + "_ewf"], shell=True)
        os.rmdir(mount_point+"_ewf")



done(folder_path)


