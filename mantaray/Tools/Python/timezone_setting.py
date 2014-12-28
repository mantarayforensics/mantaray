#This script converts timezones from Windows format to LINUX format (which is used by log2timeline)

#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2011					                 #
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

### TIMEZONE SETTING ##################################################################################################

import re

#this function converts the timezone provided by the Windows registry into the Unix format required by Timescanner
def timezone_setting(line):
    print("Converting the timezone information into Unix format")

    if(re.search('Afghanistan Standard Time',line)):
        timezone = "Asia/Kabul"
        return timezone

    elif(re.search('Alaskan Standard Time',line)):
        timezone = "America/Anchorage"
        return timezone

    elif(re.search('Arab Standard Time',line)):
        timezone = "Asia/Riyadh"
        return timezone

    elif(re.search('Arabian Standard Time',line)):
        timezone = "Asia/Muscat"
        return timezone

    elif(re.search('Arabic Standard Time',line)):
        timezone = "Asia/Baghdad"
        return timezone

    elif(re.search('Argentina Standard Time',line)):
        timezone = "America/Buenos_Aires"
        return timezone

    elif(re.search('Atlantic Standard Time',line)):
        timezone = "America/Halifax"
        return timezone

    elif(re.search('AUS Eastern Standard Time',line)):
        timezone = "Australia/Sydney"
        return timezone

    elif(re.search('Azerbaijan Standard Time',line)):
        timezone = "Asia/Baku"
        return timezone

    elif(re.search('Azores Standard Time',line)):
        timezone = "Atlantic/Azores"
        return timezone

    elif(re.search('Bangladesh Standard Time',line)):
        timezone = "Asia/Dhaka"
        return timezone

    elif(re.search('Canada Central Standard Time',line)):
        timezone = "America/Regina"
        return timezone

    elif(re.search('Cape Verde Standard Time',line)):
        timezone = "Atlantic/Cape Verde"
        return timezone

    elif(re.search('Caucasus Standard Time',line)):
        timezone = "Asia/Yerevan"
        return timezone

    elif(re.search('Cen. Australia Standard Time',line)):
        timezone = "Australia/Adelaide"
        return timezone

    elif(re.search('Central America Standard Time',line)):
        timezone = "America/Regina"
        return timezone

    elif(re.search('Central Asia Standard Time',line)):
        timezone = "Asia/Dhaka"
        return timezone

    elif(re.search('Central Europe Standard Time',line)):
        timezone = "Europe/Prague"
        return timezone

    elif(re.search('Central European Standard Time',line)):
        timezone = "Europe/Belgrade"
        return timezone

    elif(re.search('Central Pacific Standard Time',line)):
        timezone = "Pacific/Guadalcanal"
        return timezone

    elif(re.search('Central Standard Time',line)):
        timezone = "America/Chicago"
        return timezone

    elif(re.search('Central Standard Time (Mexico)',line)):
        timezone = "America/Mexico_City"
        return timezone

    elif(re.search('China Standard Time',line)):
        timezone = "Asia/Shanghai"
        return timezone

    elif(re.search('Dateline Standard Time',line)):
        timezone = "Kwajalein"
        return timezone

    elif(re.search('E. Africa Standard Time',line)):
        timezone = "Africa/Nairobi"
        return timezone

    elif(re.search('E. Australia Standard Time',line)):
        timezone = "Australia/Brisbane"
        return timezone

    elif(re.search('E. Europe Standard Time',line)):
        timezone = "Europe/Bucharest"
        return timezone

    elif(re.search('E. South America Standard Time',line)):
        timezone = "America/Sao_Paulo"
        return timezone

    elif(re.search('Eastern Standard Time',line)):
        timezone = "America/New_York"
        return timezone

    elif(re.search('Egypt Standard Time',line)):
        timezone = "Africa/Cairo"
        return timezone

    elif(re.search('Ekaterinburg Standard Time',line)):
        timezone = "Asia/Yekaterinburg"
        return timezone

    elif(re.search('Fiji Standard Time',line)):
        timezone = "Pacific/Fiji"
        return timezone

    elif(re.search('FLE Standard Time',line)):
        timezone = "Europe/Helsinki"
        return timezone

    elif(re.search('Georgian Standard Time',line)):
        timezone = "Asia/Tbilisi"
        return timezone

    elif(re.search('GMT Standard Time',line)):
        timezone = "Europe/London"
        return timezone

    elif(re.search('Greenland Standard Time',line)):
        timezone = "America/Godthab"
        return timezone

    elif(re.search('Greenwich Standard Time',line)):
        timezone = "GMT"
        return timezone

    elif(re.search('GTB Standard Time',line)):
        timezone = "Europe/Athens"
        return timezone

    elif(re.search('Hawaiian Standard Time',line)):
        timezone = "Pacific/Honolulu"
        return timezone

    elif(re.search( 'India Standard Time',line)):
        timezone = "Asia/Calcutta"
        return timezone

    elif(re.search( 'Iran Standard Time',line)):
        timezone = "Asia/Tehran"
        return timezone

    elif(re.search( 'Israel Standard Time',line)):
        timezone = "Asia/Jerusalem"
        return timezone

    elif(re.search('Jordan Standard Time',line)):
        timezone = "Asia/Amman"
        return timezone

    elif(re.search('Korea Standard Time',line)):
        timezone = "Asia/Seoul"
        return timezone

    elif(re.search('Mauritius Standard Time',line)):
        timezone = "Indian/Mauritius"
        return timezone

    elif(re.search('Mid-Atlantic Standard Time',line)):
        timezone = "Atlantic/South_Georgia"
        return timezone

    elif(re.search('Middle East Standard Time',line)):
        timezone = "Asia/Beirut"
        return timezone

    elif(re.search('Montevideo Standard Time',line)):
        timezone = "America/Montevideo"
        return timezone

    elif(re.search('Morocco Standard Time',line)):
        timezone = "Africa/Casablanca"
        return timezone

    elif(re.search('Mountain Standard Time',line)):
        timezone = "America/Denver"
        return timezone

    elif(re.search('Mountain Standard Time (Mexico)',line)):
        timezone = "America/Chihuahua"
        return timezone

    elif(re.search('Myanmar Standard Time',line)):
        timezone = "Asia/Rangoon"
        return timezone

    elif(re.search('N. Central Asia Standard Time',line)):
        timezone = "Asia/Novosibirsk"
        return timezone

    elif(re.search('Namibia Standard Time',line)):
        timezone = "Asia/Windhoek"
        return timezone

    elif(re.search('Nepal Standard Time',line)):
        timezone = "Asia/Katmandu"
        return timezone

    elif(re.search('New Zealand Standard Time',line)):
        timezone = "Pacific/Auckland"
        return timezone

    elif(re.search('Newfoundland Standard Time',line)):
        timezone = "America/St_Johns"
        return timezone

    elif(re.search('North Asia Standard Time',line)):
        timezone = "Asia/Krasnoyarsk"
        return timezone

    elif(re.search('Pacific SA Standard Time',line)):
        timezone = "America/Santiago"
        return timezone

    elif(re.search('Pacific Standard Time',line)):
        timezone = "America/Los_Angeles"
        return timezone

    elif(re.search('Pacific Standard Time (Mexico)',line)):
        timezone = "America/Tijuana"
        return timezone

    elif(re.search('Pakistan Standard Time',line)):
        timezone = "Asia/Karachi"
        return timezone

    elif(re.search('Paraguay Standard Time',line)):
        timezone = "America/Asuncion"
        return timezone

    elif(re.search('Romance Standard Time',line)):
        timezone = "Europe/Paris"
        return timezone

    elif(re.search('Russian Standard Time',line)):
        timezone = "Europe/Moscow"
        return timezone

    elif(re.search('SA Eastern Standard Time',line)):
        timezone = "America/Argentina/Buenos_Aires"
        return timezone

    elif(re.search('SA Pacific Standard Time',line)):
        timezone = "America/Bogota"
        return timezone

    elif(re.search('SA Western Standard Time',line)):
        timezone = "America/Caracas"
        return timezone

    elif(re.search('Samoa Standard Time',line)):
        timezone = "Pacific/Apia"
        return timezone

    elif(re.search('SE Asia Standard Time',line)):
        timezone = "Asia/Bangkok"
        return timezone

    elif(re.search('Singapore Standard Time',line)):
        timezone = "Asia/Singapore"
        return timezone

    elif(re.search('South Africa Standard Time',line)):
        timezone = "Africa/Harare"
        return timezone

    elif(re.search('Sri Lanka Standard Time',line)):
        timezone = "Asia/Colombo"
        return timezone

    elif(re.search('Taipei Standard Time',line)):
        timezone = "Asia/Taipei"
        return timezone

    elif(re.search('Tasmania Standard Time',line)):
        timezone = "Australia/Hobart"
        return timezone

    elif(re.search('Tokyo Standard Time',line)):
        timezone = "Asia/Tokyo"
        return timezone

    elif(re.search('Tonga Standard Time',line)):
        timezone = "Pacific/Tongatapu"
        return timezone

    elif(re.search('Ulaanbaatar Standard Time',line)):
        timezone = "Asia/Ulaanbaatar"
        return timezone

    elif(re.search('US Eastern Standard Time',line)):
        timezone = "America',line))ndianapolis"
        return timezone

    elif(re.search('US Mountain Standard Time',line)):
        timezone = "America/Phoenix"
        return timezone

    elif(re.search('UTC-11',line)):
        timezone = "Pacific/Samoa"
        return timezone

    elif(re.search('Venezuela Standard Time',line)):
        timezone = "America/Caracas"
        return timezone

    elif(re.search('Vladivostok Standard Time',line)):
        timezone = "Asia/Vladivostok"
        return timezone

    elif(re.search('W. Australia Standard Time',line)):
        timezone = "Australia/Perth"
        return timezone

    elif(re.search('W. Central Africa Standard Time',line)):
        timezone = "Africa/Luanda"
        return timezone

    elif(re.search('W. Europe Standard Time',line)):
        timezone = "Europe/Dublin"
        return timezone

    elif(re.search('West Asia Standard Time',line)):
        timezone = "Asia/Karachi"
        return timezone

    elif(re.search('West Pacific Standard Time',line)):
        timezone = "Pacific/Guam"
        return timezone

    elif(re.search('Yakutsk Standard Time',line)):
        timezone = "Asia/Yakutsk"
        return timezone

    else:
        timezone = "NONE"
        return timezone

### TIMEZONE SETTING ##################################################################################################

