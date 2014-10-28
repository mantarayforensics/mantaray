
#########################COPYRIGHT INFORMATION############################
#Copyright (C) 2014, Chapin Bryce, webmaster@mantarayforensics.com		 #
#                                                                        #
#This program is free software: you can redistribute it and/or modify    #
#it under the terms of the GNU General Public License as published by    #
#the Free Software Foundation, either version 3 of the License, or       #
#(at your option) any later version.                                     #
#                                                                        #
#This program is distributed in the hope that it will be useful,         #
#but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#GNU General Public License for more details.                            #
#                                                                        #
#You should have received a copy of the GNU General Public License       #
#along with this program.  If not, see http://www.gnu.org/licenses/.     #
#########################COPYRIGHT INFORMATION############################


import subprocess


def get_pids(fin, profile):
    pslist_plugin = "pslist"
    if profile.startswith("Lin"):
        pslist_plugin = "linux_pslist"
    elif profile.startswith("Mac"):
        pslist_plugin = "mac_pslist"
    elif profile.startswith("Win"):
        pslist_plugin = "pslist"

    awk_str = """awk '{print $2","$3","$9","$10","$4","$5","$6","$7","$8","$1}'"""
    get_pids_cmd = "vol.py -f " + fin + " --profile=" + profile + " " + pslist_plugin + " | " + awk_str

    pslists = subprocess.check_output([get_pids_cmd], shell=True)
    pslists = pslists.decode()
    pslist_array = pslists.split()

    pids = []
    pslist_dict = {}

    for count, item in enumerate(pslist_array):
        if count == 0:
            column_names_array = item.split(',')
        else:
            item2 = item.split(',')
            for count2, item3 in enumerate(item2):
                pslist_dict[column_names_array[count2].lower()] = item3

            pids.append(pslist_dict)
            pslist_dict = {}

    return pids

if __name__ == "__main__":
    import sys
    import pprint

    pprint.pprint(get_pids(sys.argv[1], sys.argv[2]))


