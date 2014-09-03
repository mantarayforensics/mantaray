#!/usr/bin/env python


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


__author__ = 'cbryce'


import subprocess
import threading
import argparse
import time
import datetime


# removed kpcrscan for the time being
plugins = ["atoms","atomscan","auditpol","bigpools","bioskbd","callbacks","clipboard","cmdline",
           "cmdscan","connections","connscan","consoles","crashinfo","deskscan","devicetree","dlllist",
           "driverirp","driverscan","envars","eventhooks","evtlogs","filescan","gahti",
           "gditimers","gdt","getservicesids","getsids","handles","hibinfo","hivelist",
           "hivescan","hpakextract","hpakinfo","idt","iehistory","imageinfo","impscan","joblinks","kdbgscan",
           "ldrmodules","limeinfo","machoinfo","malfind","mbrparser","memmap","messagehooks","mftparser","modscan",
           "modules","multiscan","mutantscan","netscan","notepad","objtypescan","patcher","poolpeek","pooltracker",
           "printkey","privs","pslist","psscan","pstree","psxview","screenshot","sessions",
           "shellbags","shimcache","sockets","sockscan","ssdt","strings","svcscan","symlinkscan","thrdscan","threads",
           "timeliner","timers","truecryptmaster","truecryptpassphrase","truecryptsummary","unloadedmodules",
           "userassist","userhandles","vadinfo","vadtree","vadwalk","vboxinfo","verinfo","vmwareinfo","windows",
           "wintree","wndscan","yarascan"]

# malfind needs `-y` to be specified
# impscan needs `--base` to be specified

pid_plugins = ["clipboard", "dlllist", "envars", "getsids", "handles", "iehistory", "impscan", "joblinks", "ldrmodules",
               "malfind", "memmap", "notepad", "privs", "pslist", "strings", "threads", "userhandles", "vadinfo",
               "vadtree", "vadwalk", "yarascan"]

parser = argparse.ArgumentParser()
parser.add_argument('fin')
parser.add_argument('profile')
parser.add_argument('-p', help="Enable processing of a specific PID across plugins")
parser.add_argument('-t', help="Specify the number of threads to run")
parser.add_argument('out')
args = parser.parse_args()
fin = args.fin
profile = args.profile
dump = args.p
num_thread = args.t
out = args.out

start = datetime.datetime.now()
def run_plugin(fin, profile, plug, out, count, plugins):
    subprocess.call(["vol -f " + fin + " --profile=" + profile + " " + plug + " --output-file=" + out + plug + ".txt"],
                    shell=True)
    print "[Thread ", datetime.datetime.now(), "] Completed " + plug + ", ", count, " of ", len(plugins)-1

for count, plug in enumerate(plugins):
    if threading.activeCount() <= 4:
        print "[Thread ", datetime.datetime.now(), "] Starting plugin " + plug
        t = threading.Thread(target=run_plugin, args=[fin, profile, plug, out, count, plugins])
        t.start()
    else:
        time.sleep(4)

while 1:
    if threading.activeCount() == 1:
        print "[Main ", datetime.datetime.now(), "] Completed"
        print "[Main ", datetime.datetime.now(), "] Runtime: ", datetime.datetime.now()-start
        break
    else:
        if time.time() % 120 == 0:  # Wait 2 minutes to prompt the user that threads are still running
            print "[Main ", datetime.datetime.now(), "] waiting for ", threading.activeCount()-1, " threads to finish"