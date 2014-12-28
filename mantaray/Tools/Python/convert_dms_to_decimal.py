#Get GPS information using exiftool and convert it from degrees to decimal
#input: Absolute path to file
#Output: List containing latitude in decimal, longitude in decimal

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 						                 #
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
import re

def convert_dms_to_decimal(quoted_full_path, extension):

    #initialize variables
    dms_list = []
    decimal = []
    valid_gps_coordinates = "YES"

    print ("The filename passed to the dms_convert function is: " + quoted_full_path)
    dms_info = subprocess.check_output(["exiftool -ext " + extension + " " + quoted_full_path + " | grep 'GPS Position' | awk '{print $4, $6, $7, $8, $9, $11, $12, $13}'"], shell=True, universal_newlines=True)
    #split dms_info on space
    dms_list = dms_info.split(' ')
    #a vaild GPS location has 7 items (0 relative) in the list.  If the dms_list doesn't have 7 items in it
    #then it is invalide
    len_dms_list = len(dms_list)
    print("Number of GPS data points is: " + str(len_dms_list))
    if (len_dms_list == 8):

        for item in dms_list:
            #check to see if item is empty, if so skip this file
            if(item == ''):
                longitude_decimal = "NULL"
                latitude_decimal = "NULL"
                valid_gps_coordinates = "NO"
                print("The GPS coordinates for this file are invalid")
            #strip out ' from item
            if(re.search(",",item)):
                item = item.replace(",","")
            if(re.search("'", item)):
                item_string = str(item)
                item_new = item_string.replace("'",'')
                decimal.append(item_new)
            elif(re.search('"', item)):
                item_new = str(item).replace('\"','')
                decimal.append(item_new)
            elif(re.search(',', item)):
                item_new = str(item).replace(',','')
                decimal.append(item_new)
            elif(item == "deg"):
                item = "0"
            else:
                decimal.append(item)
    else:
        print("The GPS coordinates should have 8 data points, this one only has: " + str(len_dms_list))
        longitude_decimal = "NULL"
        latitude_decimal = "NULL"
        valid_gps_coordinates = "NO"

    if(valid_gps_coordinates == "YES"):
        #assign variables
        latitude_degrees = decimal[0]
        print("The latitude_degrees is: " + latitude_degrees)
        latitude_minutes = decimal[1]
        print("The latitude_minutes is: " + latitude_minutes)
        latitude_seconds = decimal[2]
        print("The latitude_seconds is: " + latitude_seconds)
        latitude_direction = decimal[3]
        print("The latitude direction is: " + latitude_direction)
        longitude_degrees = decimal[4]
        print("The longitude_degrees is: " + longitude_degrees)
        longitude_minutes = decimal[5]
        print("The longitude_minutes is: " + longitude_minutes)
        longitude_seconds = decimal[6]
        print("The longitude_seconds is: " + longitude_seconds)
        longitude_direction = decimal[7]
        longitude_direction = longitude_direction.strip()
        print("The longitude direction is: " + longitude_direction)

        #do the math to convert from dms to decimal
        #convert latitude_information into degrees
        latitude_minutes_degrees = float(latitude_minutes) * (1/60)
        print("Latitude minutes converted into degrees is: " + str(latitude_minutes_degrees))
        latitude_seconds_degrees = float(latitude_seconds) * (1/3600)
        print("Latitude seconds converted into degrees is: " + str(latitude_seconds_degrees))
        latitude_decimal = int(latitude_degrees) + latitude_minutes_degrees + latitude_seconds_degrees

        #make latitude negative if latitude_direction = S
        if(latitude_direction == "S"):
            latitude_decimal = latitude_decimal * -1
        print("Latitude in degrees is: " + str(latitude_decimal))

        #convert longitude information into degrees
        longitude_minutes_degrees = float(longitude_minutes) * (1/60)
        print("Longitude minutes converted into degrees is: " + str(longitude_minutes_degrees))
        longitude_seconds_degrees = float(longitude_seconds) * (1/3600)
        print("Longitude seconds converted into degrees is: " + str(longitude_seconds_degrees))
        longitude_decimal = int(longitude_degrees) + longitude_minutes_degrees + longitude_seconds_degrees

        if(longitude_direction == "W"):
            longitude_decimal = (longitude_decimal * -1)
        print("Longitude in degrees is: " + str(longitude_decimal))

    return (latitude_decimal, longitude_decimal)

