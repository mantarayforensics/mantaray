#!/usr/bin/env python

__author__ = 'mantaray'


import subprocess
import threading
import argparse
import time
import datetime



plugins = ["atoms","atomscan","auditpol","bigpools","bioskbd","callbacks","clipboard","cmdline",
           "cmdscan","connections","connscan","consoles","crashinfo","deskscan","devicetree","dlllist",
           "driverirp","driverscan","envars","eventhooks","evtlogs","filescan","gahti",
           "gditimers","gdt","getservicesids","getsids","handles","hibinfo","hivelist",
           "hivescan","hpakextract","hpakinfo","idt","iehistory","imageinfo","impscan","joblinks","kdbgscan","kpcrscan",
           "ldrmodules","limeinfo","machoinfo","malfind","mbrparser","memmap","messagehooks","mftparser","modscan",
           "modules","multiscan","mutantscan","netscan","notepad","objtypescan","patcher","poolpeek","pooltracker",
           "printkey","privs","pslist","psscan","pstree","psxview","screenshot","sessions",
           "shellbags","shimcache","sockets","sockscan","ssdt","strings","svcscan","symlinkscan","thrdscan","threads",
           "timeliner","timers","truecryptmaster","truecryptpassphrase","truecryptsummary","unloadedmodules",
           "userassist","userhandles","vadinfo","vadtree","vadwalk","vboxinfo","verinfo","vmwareinfo","windows",
           "wintree","wndscan","yarascan"]

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
        if time.time() % 60 == 0:
            print "[Main ", datetime.datetime.now(), "] waiting for ", threading.activeCount()-1, " threads to finish"